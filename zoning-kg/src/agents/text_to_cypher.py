"""Text-to-Cypher agent: Converts natural language to Cypher queries with retry logic."""

from openai import OpenAI
from typing import Optional, Tuple, List
from dataclasses import dataclass
from .config import get_openai_api_key


@dataclass
class CypherAttempt:
    """Record of a Cypher generation attempt."""
    iteration: int
    cypher: str
    result_count: int
    error: Optional[str]
    refinement_reason: Optional[str]


TEXT_TO_CYPHER_SYSTEM_PROMPT = """You are a Cypher query generator for a Neo4j zoning knowledge graph.

## Graph Schema

### Node Labels:
- **Jurisdiction**: name, level (city/county/state), jurisdiction_id, display_name
- **Zone**: code (SF-5, MF-4, etc), name, family (single_family/multifamily/commercial), zone_id, display_name
- **UseType**: name, group (residential/commercial/industrial), use_type_id, display_name, aliases
- **Rule**: section, title, applies_to_uses[], applies_in_zones[], summary, text_excerpt
- **Constraint**: metric, constraint_value, unit, applies_to (lot/site/building/unit), operator, summary, source_text
- **Condition**: condition_field, condition_value, operator
- **Override**: bill_id (SB-840, SB-2835), metric, override_type (floor/ceiling), override_value, scope_zones, scope_uses
- **DocumentSource**: document, section, subsection, text_excerpt

### Relationship:
All relationships use `RELATES_TO` with a `name` property indicating the semantic type:
- ALLOWS_USE: Zone allows a UseType (has permitted_by_right, requires_conditional_use, requires_special_exception)
- CONTAINS: Jurisdiction contains Zone
- HAS_CONSTRAINT: Rule has Constraint
- HAS_CONDITION: Constraint has Condition
- APPLIES_IN: Rule applies in Zone
- OVERRIDDEN_BY: Constraint overridden by Override
- SOURCED_FROM: Entity sourced from DocumentSource
- GOVERNS, GOVERNED_BY, DEFINES, etc.

### Relationship Properties:
- `name`: semantic relationship type (ALLOWS_USE, HAS_CONSTRAINT, etc.)
- `fact`: textual description of the relationship
- `permitted_by_right`: boolean
- `requires_conditional_use`: boolean
- `requires_special_exception`: boolean

## Your Task

Given a natural language question about zoning, generate ONE Cypher query that retrieves the relevant data.

Rules:
1. Use RELATES_TO as the relationship type, filter by r.name for semantic type
2. Return relevant properties, not just nodes
3. Use toLower() for case-insensitive matching
4. Limit results to 50 unless the question asks for counts
5. Include relationship properties like permitted_by_right, fact when relevant
6. For zone codes like SF-5, MF-4, match on z.code or z.zone_id
7. For use types, match on u.name, u.use_type_id, or u.display_name
8. Be flexible with matching - use CONTAINS for partial matches

Output ONLY the Cypher query, no explanation.

## Examples

Question: "Can I build townhouses in SF-5?"
```cypher
MATCH (z:Zone)-[r:RELATES_TO]->(u:UseType)
WHERE toLower(z.code) = 'sf-5' 
  AND (toLower(u.name) CONTAINS 'townhouse' OR toLower(u.use_type_id) CONTAINS 'townhouse')
RETURN z.code AS zone, z.display_name AS zone_name, 
       u.name AS use_type, u.display_name AS use_display,
       r.name AS relationship, r.permitted_by_right AS by_right,
       r.requires_conditional_use AS conditional, r.requires_special_exception AS special_exception,
       r.fact AS fact
LIMIT 20
```

Question: "What are the height constraints for MF-4?"
```cypher
MATCH (z:Zone)-[r1:RELATES_TO]->(rule:Rule)-[r2:RELATES_TO]->(c:Constraint)
WHERE toLower(z.code) = 'mf-4' AND toLower(c.metric) CONTAINS 'height'
RETURN z.code AS zone, rule.name AS rule_name, rule.section AS section,
       c.name AS constraint, c.metric AS metric, c.constraint_value AS value,
       c.unit AS unit, c.operator AS operator, c.source_text AS source
LIMIT 20
```

Question: "What zones allow townhouses?"
```cypher
MATCH (z:Zone)-[r:RELATES_TO]->(u:UseType)
WHERE (toLower(u.name) CONTAINS 'townhouse' OR toLower(u.use_type_id) CONTAINS 'townhouse')
  AND r.name = 'ALLOWS_USE'
RETURN DISTINCT z.code AS zone, z.display_name AS zone_name, z.family AS zone_family,
       u.name AS use_type, r.permitted_by_right AS by_right
ORDER BY z.code
LIMIT 50
```

Question: "What are the setback requirements?"
```cypher
MATCH (c:Constraint)
WHERE toLower(c.metric) CONTAINS 'setback' OR toLower(c.name) CONTAINS 'setback'
RETURN c.name AS constraint, c.metric AS metric, c.constraint_value AS value,
       c.unit AS unit, c.operator AS operator, c.applies_to AS scope,
       c.source_text AS source, c.summary AS summary
LIMIT 30
```

Question: "What overrides apply from SB-840?"
```cypher
MATCH (o:Override)
WHERE toLower(o.bill_id) CONTAINS 'sb-840' OR toLower(o.name) CONTAINS 'sb-840'
RETURN o.name AS override, o.bill_id AS bill, o.metric AS metric,
       o.override_type AS type, o.override_value AS value, o.unit AS unit,
       o.scope_zones AS zones, o.scope_uses AS uses, o.summary AS summary
LIMIT 20
```
"""


REFINEMENT_PROMPT = """The previous Cypher query returned no results or had an error.

## Previous Query
```cypher
{previous_cypher}
```

## Issue
{issue}

## Original Question
{question}

Please generate a DIFFERENT Cypher query that might return results. Try:
1. Broader matching (remove specific filters, use more CONTAINS)
2. Different node types or relationships
3. Alternative property names
4. Simpler query structure

Output ONLY the new Cypher query, no explanation.
"""


class TextToCypherAgent:
    """Agent that converts natural language to Cypher queries with retry logic."""
    
    def __init__(self, max_retries: int = 3):
        self.client = OpenAI(api_key=get_openai_api_key())
        self.max_retries = max_retries
        self.attempts: List[CypherAttempt] = []
    
    def generate_cypher(self, question: str, schema_context: str = "") -> str:
        """Generate a Cypher query from natural language.
        
        Args:
            question: Natural language question about zoning
            schema_context: Optional additional schema context
            
        Returns:
            Cypher query string
        """
        system_prompt = TEXT_TO_CYPHER_SYSTEM_PROMPT
        if schema_context:
            system_prompt += f"\n\n## Additional Schema Context\n{schema_context}"
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a Cypher query for: {question}"}
            ],
            temperature=0.0,
            max_tokens=500
        )
        
        cypher = response.choices[0].message.content.strip()
        return self._clean_cypher(cypher)
    
    def refine_cypher(self, question: str, previous_cypher: str, issue: str) -> str:
        """Generate a refined Cypher query after a failed attempt.
        
        Args:
            question: Original natural language question
            previous_cypher: The query that failed or returned no results
            issue: Description of what went wrong
            
        Returns:
            Refined Cypher query string
        """
        prompt = REFINEMENT_PROMPT.format(
            previous_cypher=previous_cypher,
            issue=issue,
            question=question
        )
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": TEXT_TO_CYPHER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Slightly higher for variation
            max_tokens=500
        )
        
        cypher = response.choices[0].message.content.strip()
        return self._clean_cypher(cypher)
    
    def _clean_cypher(self, cypher: str) -> str:
        """Remove markdown code blocks from Cypher."""
        if cypher.startswith("```"):
            lines = cypher.split("\n")
            # Remove first line (```cypher) and last line (```)
            if lines[-1].strip() == "```":
                cypher = "\n".join(lines[1:-1])
            else:
                cypher = "\n".join(lines[1:])
        return cypher.strip()
    
    def record_attempt(self, iteration: int, cypher: str, result_count: int, 
                       error: Optional[str] = None, refinement_reason: Optional[str] = None):
        """Record an attempt for debugging."""
        self.attempts.append(CypherAttempt(
            iteration=iteration,
            cypher=cypher,
            result_count=result_count,
            error=error,
            refinement_reason=refinement_reason
        ))
    
    def clear_attempts(self):
        """Clear attempt history."""
        self.attempts = []
    
    def get_attempts_summary(self) -> str:
        """Get a summary of all attempts."""
        if not self.attempts:
            return "No attempts recorded."
        
        lines = []
        for attempt in self.attempts:
            status = "✓" if attempt.result_count > 0 and not attempt.error else "✗"
            lines.append(f"  Attempt {attempt.iteration}: {status} ({attempt.result_count} results)")
            if attempt.error:
                lines.append(f"    Error: {attempt.error[:100]}")
            if attempt.refinement_reason:
                lines.append(f"    Refined because: {attempt.refinement_reason}")
        return "\n".join(lines)
