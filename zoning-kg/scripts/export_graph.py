#!/usr/bin/env python3
"""
Export comprehensive knowledge graph documentation.
Creates zoning_kg.md - Complete graph documentation for LLM context
"""

import os
import json
from datetime import datetime
from dotenv import dotenv_values
from neo4j import GraphDatabase

env = dotenv_values('.env')
driver = GraphDatabase.driver(env['NEO4J_URI'], auth=(env['NEO4J_USER'], env['NEO4J_PASSWORD']))


def get_stats(session):
    """Get overall graph statistics."""
    stats = {}
    stats['total_nodes'] = session.run('MATCH (n) RETURN count(n) as c').single()['c']
    stats['total_relationships'] = session.run('MATCH ()-[r]->() RETURN count(r) as c').single()['c']
    stats['episodes'] = session.run('MATCH (n:Episodic) RETURN count(n) as c').single()['c']
    return stats


def get_label_counts(session):
    """Get node counts by label."""
    counts = {}
    res = session.run('CALL db.labels() YIELD label RETURN label')
    labels = [r['label'] for r in res]
    for label in labels:
        # Skip invalid labels
        if '$' in label or label.startswith('_'):
            continue
        try:
            count = session.run(f'MATCH (n:`{label}`) RETURN count(n) as c').single()['c']
            if count > 0:
                counts[label] = count
        except:
            pass
    return counts


def get_rel_type_counts(session):
    """Get relationship type counts."""
    res = session.run('MATCH ()-[r]->() RETURN type(r) as t, count(*) as c ORDER BY c DESC')
    return {r['t']: r['c'] for r in res}


def get_edge_type_counts(session):
    """Get edge type (r.name) counts for RELATES_TO."""
    res = session.run('''
        MATCH ()-[r:RELATES_TO]->()
        RETURN r.name as edge, count(*) as c
        ORDER BY c DESC
    ''')
    return {r['edge']: r['c'] for r in res}


def get_node_properties(session, label):
    """Get property keys for a node type (excluding embeddings)."""
    res = session.run(f'MATCH (n:`{label}`) RETURN keys(n) as props LIMIT 1')
    rec = res.single()
    if rec:
        return [p for p in rec['props'] if 'embedding' not in p.lower()]
    return []


def get_sample_nodes(session, label, limit=5):
    """Get sample nodes of a given label."""
    res = session.run(f'''
        MATCH (n:`{label}`)
        RETURN n.name as name, n.summary as summary, properties(n) as props
        LIMIT {limit}
    ''')
    return [dict(r) for r in res]


def get_all_nodes_of_type(session, label):
    """Get all nodes of a given label with key properties."""
    res = session.run(f'''
        MATCH (n:`{label}`)
        RETURN n.name as name, n.summary as summary
        ORDER BY n.name
    ''')
    return [dict(r) for r in res]


def get_relationship_patterns(session):
    """Get common relationship patterns."""
    res = session.run('''
        MATCH (a)-[r:RELATES_TO]->(b)
        WITH labels(a)[0] as from_type, r.name as edge, labels(b)[0] as to_type, count(*) as cnt
        WHERE cnt > 5
        RETURN from_type, edge, to_type, cnt
        ORDER BY cnt DESC
        LIMIT 50
    ''')
    return [dict(r) for r in res]


def get_property_values(session, label, prop_name, limit=20):
    """Get sample values for a property."""
    res = session.run(f'''
        MATCH (n:`{label}`)
        WHERE n.`{prop_name}` IS NOT NULL
        RETURN DISTINCT n.`{prop_name}` as value
        LIMIT {limit}
    ''')
    return [r['value'] for r in res]


def generate_markdown(session):
    """Generate comprehensive markdown documentation."""
    md = []
    
    # Header
    md.append('# ORGAnIZM Zoning Knowledge Graph - Complete Documentation')
    md.append('')
    md.append('**Comprehensive Graph Documentation for LLM Context**')
    md.append('')
    md.append('This document provides complete information about the Austin Zoning Knowledge Graph,')
    md.append('including all entity types, their properties, sample values, relationships, and query patterns.')
    md.append('Use this as context to understand and query the graph.')
    md.append('')
    md.append(f'*Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*')
    md.append('')
    md.append('---')
    md.append('')
    
    # Overview
    stats = get_stats(session)
    md.append('## 1. Graph Overview')
    md.append('')
    md.append('This knowledge graph represents the **Austin, Texas Land Development Code (LDC)**')
    md.append('and **Texas state housing bills (SB-840, SB-2835)** as a structured graph database.')
    md.append('')
    md.append('### Statistics')
    md.append('')
    md.append('| Metric | Value |')
    md.append('|--------|-------|')
    md.append(f'| Total Nodes | {stats["total_nodes"]:,} |')
    md.append(f'| Total Relationships | {stats["total_relationships"]:,} |')
    md.append(f'| Episodes Ingested | {stats["episodes"]} |')
    md.append('')
    
    # Node Types
    md.append('---')
    md.append('')
    md.append('## 2. Node Types (Labels)')
    md.append('')
    label_counts = get_label_counts(session)
    md.append('| Label | Count | Description |')
    md.append('|-------|-------|-------------|')
    
    descriptions = {
        'Jurisdiction': 'Geographic authority (city, county, state) that issues regulations',
        'Zone': 'Zoning district classification (SF-1, MF-4, CBD, etc.)',
        'UseType': 'Building/development use category (residential, commercial, etc.)',
        'Rule': 'Regulation section from the Land Development Code',
        'Constraint': 'Quantitative requirement (min/max values for setbacks, height, etc.)',
        'Condition': 'Contextual trigger for when constraints apply',
        'Override': 'State law that supersedes local regulations',
        'DocumentSource': 'Citation/source reference for traceability',
        'Entity': 'Generic/untyped entities extracted by LLM',
        'Episodic': 'Ingested text episodes (source content)',
    }
    
    for label, count in sorted(label_counts.items(), key=lambda x: -x[1]):
        desc = descriptions.get(label, '')
        md.append(f'| {label} | {count:,} | {desc} |')
    md.append('')
    
    # Detailed Entity Schemas
    md.append('---')
    md.append('')
    md.append('## 3. Entity Type Schemas')
    md.append('')
    md.append('Detailed schema for each ontology entity type including properties and sample values.')
    md.append('')
    
    ontology_types = ['Jurisdiction', 'Zone', 'UseType', 'Rule', 'Constraint', 'Condition', 'Override', 'DocumentSource']
    
    for label in ontology_types:
        count = label_counts.get(label, 0)
        if count == 0:
            continue
            
        md.append(f'### 3.{ontology_types.index(label)+1}. {label}')
        md.append('')
        md.append(f'**Count:** {count} nodes')
        md.append('')
        md.append(f'**Description:** {descriptions.get(label, "N/A")}')
        md.append('')
        
        # Properties with sample values
        props = get_node_properties(session, label)
        if props:
            md.append('**Properties:**')
            md.append('')
            md.append('| Property | Sample Values |')
            md.append('|----------|---------------|')
            for p in sorted(props):
                if p in ['uuid', 'group_id', 'created_at', 'labels']:
                    continue  # Skip internal props
                values = get_property_values(session, label, p, 3)
                if values:
                    # Truncate long values
                    sample_str = ', '.join([str(v)[:50] for v in values[:3]])
                    md.append(f'| `{p}` | {sample_str} |')
            md.append('')
        
        # All entities for small types
        if count <= 30:
            md.append(f'**All {label} Entities:**')
            md.append('')
            all_nodes = get_all_nodes_of_type(session, label)
            for node in all_nodes:
                name = node['name'] if node['name'] else 'N/A'
                md.append(f'- **{name}**')
            md.append('')
        else:
            # Sample nodes for large types
            md.append('**Sample Entities:**')
            md.append('')
            samples = get_sample_nodes(session, label, 5)
            for i, sample in enumerate(samples, 1):
                name = sample['name'][:80] if sample['name'] else 'N/A'
                md.append(f'{i}. **{name}**')
                if sample.get('summary'):
                    summary = sample['summary'][:200]
                    md.append(f'   - {summary}...')
            md.append('')
        md.append('')
    
    # Relationship Types
    md.append('---')
    md.append('')
    md.append('## 4. Relationship Types')
    md.append('')
    
    rel_counts = get_rel_type_counts(session)
    md.append('### 4.1. Neo4j Relationship Types')
    md.append('')
    md.append('| Type | Count | Description |')
    md.append('|------|-------|-------------|')
    rel_descs = {
        'RELATES_TO': 'Semantic relationship with name property',
        'MENTIONS': 'Episode mentions entity',
    }
    for rel, count in rel_counts.items():
        desc = rel_descs.get(rel, '')
        md.append(f'| `{rel}` | {count:,} | {desc} |')
    md.append('')
    
    # Edge Types (r.name)
    md.append('### 4.2. Semantic Edge Types')
    md.append('')
    md.append('The `RELATES_TO` relationships have a `name` property indicating semantic meaning.')
    md.append('')
    
    edge_counts = get_edge_type_counts(session)
    md.append('| Edge Type | Count | Description |')
    md.append('|-----------|-------|-------------|')
    
    edge_descriptions = {
        'APPLIES_IN': 'Rule/Constraint applies in a specific zone',
        'CONTAINS': 'Jurisdiction contains zone; Zone contains subzone',
        'SOURCED_FROM': 'Entity traced back to source document',
        'GOVERNED_BY': 'Use type is governed by a rule',
        'ALLOWS_USE': 'Zone permits a use type',
        'HAS_CONSTRAINT': 'Rule has a quantitative constraint',
        'HAS_CONDITION': 'Constraint has a conditional trigger',
        'OVERRIDDEN_BY': 'Local rule overridden by state law',
        'REQUIRES': 'Conditional requirement',
        'DEFINES': 'Definition relationship',
        'INCLUDES': 'Inclusion relationship',
        'REFERENCES': 'Cross-reference to another section',
    }
    
    for edge, count in list(edge_counts.items())[:25]:
        desc = edge_descriptions.get(edge, '')
        md.append(f'| `{edge}` | {count:,} | {desc} |')
    
    if len(edge_counts) > 25:
        md.append(f'| ... | ... | *({len(edge_counts) - 25} more edge types)* |')
    md.append('')
    
    # Relationship Patterns
    md.append('### 4.3. Common Relationship Patterns')
    md.append('')
    md.append('| From Type | Edge | To Type | Count |')
    md.append('|-----------|------|---------|-------|')
    
    patterns = get_relationship_patterns(session)
    for p in patterns[:25]:
        md.append(f'| {p["from_type"]} | `{p["edge"]}` | {p["to_type"]} | {p["cnt"]} |')
    md.append('')
    
    # Query Examples
    md.append('---')
    md.append('')
    md.append('## 5. Query Examples')
    md.append('')
    
    md.append('### 5.1. Find all zones in Austin')
    md.append('```cypher')
    md.append('MATCH (j:Jurisdiction)-[r:RELATES_TO]->(z:Zone)')
    md.append("WHERE r.name = 'CONTAINS' AND j.name CONTAINS 'Austin'")
    md.append('RETURN z.name, z.code, z.family')
    md.append('ORDER BY z.name')
    md.append('```')
    md.append('')
    
    md.append('### 5.2. Find zones that allow townhouses')
    md.append('```cypher')
    md.append('MATCH (z:Zone)-[r:RELATES_TO]->(u:UseType)')
    md.append("WHERE r.name = 'ALLOWS_USE' AND u.name CONTAINS 'Townhouse'")
    md.append('RETURN z.name, u.name')
    md.append('```')
    md.append('')
    
    md.append('### 5.3. Get constraints for a specific zone')
    md.append('```cypher')
    md.append('MATCH (z:Zone)-[:RELATES_TO]-(r:Rule)-[rel:RELATES_TO]->(c:Constraint)')
    md.append("WHERE z.name CONTAINS 'SF-5' AND rel.name = 'HAS_CONSTRAINT'")
    md.append('RETURN z.name, r.name, c.name, c.summary')
    md.append('```')
    md.append('')
    
    md.append('### 5.4. Find all state overrides')
    md.append('```cypher')
    md.append('MATCH (o:Override)')
    md.append('RETURN o.name, o.bill_id, o.metric, o.override_value, o.summary')
    md.append('```')
    md.append('')
    
    md.append('### 5.5. Trace a rule to its source document')
    md.append('```cypher')
    md.append('MATCH (r:Rule)-[rel:RELATES_TO]->(d:DocumentSource)')
    md.append("WHERE rel.name = 'SOURCED_FROM'")
    md.append('RETURN r.name, r.section, d.document, d.section')
    md.append('LIMIT 10')
    md.append('```')
    md.append('')
    
    md.append('### 5.6. Find rules that apply in multiple zones')
    md.append('```cypher')
    md.append('MATCH (r:Rule)-[rel:RELATES_TO]->(z:Zone)')
    md.append("WHERE rel.name = 'APPLIES_IN'")
    md.append('WITH r, count(z) as zone_count')
    md.append('WHERE zone_count > 3')
    md.append('RETURN r.name, zone_count')
    md.append('ORDER BY zone_count DESC')
    md.append('```')
    md.append('')
    
    md.append('### 5.7. Full graph visualization query')
    md.append('```cypher')
    md.append('MATCH path = (j:Jurisdiction)-[:RELATES_TO*1..3]->(n)')
    md.append("WHERE j.name CONTAINS 'Austin'")
    md.append('RETURN path')
    md.append('LIMIT 100')
    md.append('```')
    md.append('')
    
    # Ontology Summary
    md.append('---')
    md.append('')
    md.append('## 6. Ontology Summary')
    md.append('')
    md.append('### Entity Hierarchy')
    md.append('```')
    md.append('Jurisdiction (city, county, state)')
    md.append('├── Zone (zoning districts)')
    md.append('│   └── UseType (permitted uses)')
    md.append('│       └── Rule (regulations)')
    md.append('│           └── Constraint (quantitative limits)')
    md.append('│               └── Condition (when constraint applies)')
    md.append('└── Override (state preemptions)')
    md.append('    └── applies to local Constraints')
    md.append('```')
    md.append('')
    
    md.append('### Key Relationships')
    md.append('```')
    md.append('Jurisdiction --[CONTAINS]--> Zone')
    md.append('Zone --[ALLOWS_USE]--> UseType')
    md.append('UseType --[GOVERNED_BY]--> Rule')
    md.append('Rule --[APPLIES_IN]--> Zone')
    md.append('Rule --[HAS_CONSTRAINT]--> Constraint')
    md.append('Constraint --[HAS_CONDITION]--> Condition')
    md.append('Constraint --[OVERRIDDEN_BY]--> Override')
    md.append('* --[SOURCED_FROM]--> DocumentSource')
    md.append('```')
    md.append('')
    
    md.append('---')
    md.append('')
    md.append('## 7. Data Sources')
    md.append('')
    md.append('| Source | Description |')
    md.append('|--------|-------------|')
    md.append('| Austin LDC | Land Development Code (~103,756 lines) |')
    md.append('| Texas SB-840 | Housing in commercial areas bill |')
    md.append('| Texas SB-2835 | Transit-oriented development bill |')
    md.append('')
    md.append('---')
    md.append('')
    md.append('*End of Knowledge Graph Documentation*')
    
    return '\n'.join(md)


def main():
    with driver.session() as session:
        print('Generating zoning_kg.md...')
        md_content = generate_markdown(session)
        with open('zoning_kg.md', 'w') as f:
            f.write(md_content)
        print(f'  Saved zoning_kg.md ({len(md_content):,} bytes)')
    
    driver.close()
    print('Done!')


if __name__ == '__main__':
    main()
