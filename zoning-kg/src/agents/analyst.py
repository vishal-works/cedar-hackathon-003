"""Agent 1: Zoning Analyst - Domain expert for zoning analysis with retry logic."""

from openai import OpenAI
from typing import Tuple, Optional
from .config import ANALYST_AGENT, GRAPH_SCHEMA_CONTEXT, get_openai_api_key
from .mcp_client import get_mcp_client
from .text_to_cypher import TextToCypherAgent


class ZoningAnalyst:
    """Agent that analyzes zoning questions using graph context with retry logic."""
    
    def __init__(self, verbose: bool = False, max_retries: int = 3):
        self.client = OpenAI(api_key=get_openai_api_key())
        self.config = ANALYST_AGENT
        self.mcp = get_mcp_client()
        self.text_to_cypher = TextToCypherAgent(max_retries=max_retries)
        self.verbose = verbose
        self.max_retries = max_retries
        self.print_fn = print if verbose else lambda *a, **k: None
        
        # Build system prompt with schema context
        self.system_prompt = self.config.system_prompt.format(
            schema_context=GRAPH_SCHEMA_CONTEXT
        )
    
    def _execute_with_retry(self, question: str) -> Tuple[str, list, str]:
        """Execute text-to-cypher with retry logic.
        
        Returns:
            Tuple of (final_cypher, results, attempts_summary)
        """
        self.text_to_cypher.clear_attempts()
        
        cypher = None
        results = []
        last_error = None
        
        for iteration in range(1, self.max_retries + 1):
            # Generate or refine Cypher
            if iteration == 1:
                self.print_fn(f"\n  🔄 Iteration {iteration}: Generating initial Cypher...")
                cypher = self.text_to_cypher.generate_cypher(question)
            else:
                issue = last_error or f"Query returned 0 results"
                self.print_fn(f"\n  🔄 Iteration {iteration}: Refining query ({issue[:50]}...)")
                cypher = self.text_to_cypher.refine_cypher(question, cypher, issue)
            
            self.print_fn(f"  📝 Query:\n     {cypher[:100]}..." if len(cypher) > 100 else f"  📝 Query: {cypher}")
            
            # Execute query
            result = self.mcp.read_query(cypher)
            
            if result.success and result.data:
                results = result.data.get("results", [])
                count = result.data.get("count", 0)
                
                self.text_to_cypher.record_attempt(
                    iteration=iteration,
                    cypher=cypher,
                    result_count=count,
                    error=None,
                    refinement_reason=last_error if iteration > 1 else None
                )
                
                self.print_fn(f"  ✅ Results: {count} rows")
                
                # If we got results, we're done
                if count > 0:
                    break
                else:
                    last_error = "Query returned 0 results"
            else:
                error = result.error or "Unknown error"
                self.text_to_cypher.record_attempt(
                    iteration=iteration,
                    cypher=cypher,
                    result_count=0,
                    error=error,
                    refinement_reason=last_error if iteration > 1 else None
                )
                self.print_fn(f"  ❌ Error: {error[:80]}...")
                last_error = error
        
        attempts_summary = self.text_to_cypher.get_attempts_summary()
        return cypher, results, attempts_summary
    
    def get_graph_context(self, question: str) -> str:
        """Retrieve relevant graph data for the query with retry logic.
        
        Args:
            question: User's natural language question
            
        Returns:
            Formatted string with graph query results
        """
        context_parts = []
        
        # 1. Get schema
        schema_str = self.mcp.format_schema_for_prompt()
        context_parts.append("## Graph Schema")
        context_parts.append(schema_str)
        
        # 2. Execute with retry logic
        cypher, results, attempts_summary = self._execute_with_retry(question)
        
        context_parts.append("\n## Query Attempts")
        context_parts.append(attempts_summary)
        
        context_parts.append("\n## Final Cypher Query")
        context_parts.append(f"```cypher\n{cypher}\n```")
        
        context_parts.append(f"\n## Query Results ({len(results)} rows)")
        if results:
            context_parts.append(self.mcp.format_results_for_prompt(results))
        else:
            context_parts.append("No matching data found after all retry attempts.")
        
        return "\n".join(context_parts)
    
    def analyze(self, query: str, graph_context: str = None) -> str:
        """Analyze a zoning question.
        
        Args:
            query: User's natural language question
            graph_context: Pre-fetched graph context (optional)
            
        Returns:
            Detailed analysis in natural language
        """
        # Get graph context if not provided
        if graph_context is None:
            graph_context = self.get_graph_context(query)
        
        # Build the user message
        user_message = f"""## User Question
{query}

## Available Graph Data
{graph_context}

Please analyze this zoning question using the graph data above. Provide a thorough analysis covering permissibility, constraints, overrides, conditions, and sources. Be specific about what you found in the graph results."""
        
        # Call OpenAI
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        return response.choices[0].message.content
