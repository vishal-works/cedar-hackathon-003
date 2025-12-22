#!/usr/bin/env python3
"""
Export comprehensive knowledge graph documentation from Neo4j.
Creates zoning_kg.md - Complete graph documentation for LLM context
"""

import os
import json
from datetime import datetime
from dotenv import dotenv_values
from neo4j import GraphDatabase

env = dotenv_values('.env')
driver = GraphDatabase.driver(env['NEO4J_URI'], auth=(env['NEO4J_USER'], env['NEO4J_PASSWORD']))


def run_query(session, query):
    """Run a query and return results as list of dicts."""
    try:
        res = session.run(query)
        return [dict(r) for r in res]
    except Exception as e:
        print(f"Query error: {e}")
        return []


def generate_markdown(session):
    """Generate comprehensive markdown documentation."""
    md = []
    
    # Header
    md.append('# ORGAnIZM Zoning Knowledge Graph - Complete Documentation')
    md.append('')
    md.append('**Comprehensive Graph Documentation for LLM Context**')
    md.append('')
    md.append('This document provides complete information about the Austin Zoning Knowledge Graph,')
    md.append('including all entity types, properties, relationships, orphan nodes, and query patterns.')
    md.append('')
    md.append(f'*Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*')
    md.append('')
    md.append('---')
    md.append('')
    
    # ==========================================================================
    # 1. GRAPH OVERVIEW
    # ==========================================================================
    md.append('## 1. Graph Overview')
    md.append('')
    
    total_nodes = run_query(session, 'MATCH (n) RETURN count(n) as c')[0]['c']
    total_rels = run_query(session, 'MATCH ()-[r]->() RETURN count(r) as c')[0]['c']
    episodes = run_query(session, 'MATCH (n:Episodic) RETURN count(n) as c')[0]['c']
    
    md.append('| Metric | Value |')
    md.append('|--------|-------|')
    md.append(f'| **Total Nodes** | {total_nodes:,} |')
    md.append(f'| **Total Relationships** | {total_rels:,} |')
    md.append(f'| **Episodes Ingested** | {episodes} |')
    md.append('')
    
    # ==========================================================================
    # 2. NODE LABELS AND COUNTS
    # ==========================================================================
    md.append('---')
    md.append('')
    md.append('## 2. Node Labels')
    md.append('')
    md.append('| Label | Count | Description |')
    md.append('|-------|-------|-------------|')
    
    descriptions = {
        'Jurisdiction': 'Geographic authority (city, county, state)',
        'Zone': 'Zoning district classification (SF-1, MF-4, CBD)',
        'UseType': 'Building/development use category',
        'Rule': 'Regulation section from LDC',
        'Constraint': 'Quantitative requirement (min/max values)',
        'Condition': 'Contextual trigger for constraints',
        'Override': 'State law superseding local regulations',
        'DocumentSource': 'Citation/source reference',
        'Entity': 'Generic/untyped entities from LLM',
        'Episodic': 'Ingested text episodes',
    }
    
    # Get all labels dynamically
    labels_result = run_query(session, '''
        MATCH (n)
        WITH labels(n) as labs
        UNWIND labs as label
        WITH label WHERE NOT label STARTS WITH '$'
        RETURN DISTINCT label
    ''')
    
    label_counts = {}
    for r in labels_result:
        label = r['label']
        count_res = run_query(session, f'MATCH (n:`{label}`) RETURN count(n) as c')
        if count_res:
            label_counts[label] = count_res[0]['c']
    
    for label, count in sorted(label_counts.items(), key=lambda x: -x[1]):
        desc = descriptions.get(label, '')
        md.append(f'| `{label}` | {count:,} | {desc} |')
    md.append('')
    
    # ==========================================================================
    # 3. ENTITY TYPE SCHEMAS
    # ==========================================================================
    md.append('---')
    md.append('')
    md.append('## 3. Entity Type Schemas')
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
        
        # Get all properties for this type
        props_result = run_query(session, f'''
            MATCH (n:`{label}`)
            UNWIND keys(n) as prop
            WITH prop WHERE NOT prop CONTAINS 'embedding'
            RETURN DISTINCT prop
            ORDER BY prop
        ''')
        
        if props_result:
            md.append('**Properties:**')
            md.append('')
            md.append('| Property | Type | Sample Values |')
            md.append('|----------|------|---------------|')
            
            for r in props_result:
                prop = r['prop']
                if prop in ['uuid', 'group_id', 'labels']:
                    continue
                
                # Get sample values
                sample_res = run_query(session, f'''
                    MATCH (n:`{label}`)
                    WHERE n.`{prop}` IS NOT NULL
                    RETURN DISTINCT n.`{prop}` as val
                    LIMIT 3
                ''')
                
                if sample_res:
                    val = sample_res[0]['val']
                    val_type = type(val).__name__
                    samples = [str(r['val'])[:40] for r in sample_res[:3]]
                    sample_str = ', '.join(samples)
                    md.append(f'| `{prop}` | {val_type} | {sample_str} |')
            md.append('')
        
        # Get ALL entities for small types, sample for large
        if count <= 50:
            md.append(f'**All {label} Entities ({count}):**')
            md.append('')
            all_nodes = run_query(session, f'''
                MATCH (n:`{label}`)
                RETURN n.name as name
                ORDER BY n.name
            ''')
            for node in all_nodes:
                name = node['name'] if node['name'] else '(unnamed)'
                md.append(f'- {name}')
            md.append('')
        else:
            md.append(f'**Sample Entities (showing 10 of {count}):**')
            md.append('')
            samples = run_query(session, f'''
                MATCH (n:`{label}`)
                RETURN n.name as name, n.summary as summary
                LIMIT 10
            ''')
            for i, s in enumerate(samples, 1):
                name = s['name'][:60] if s['name'] else '(unnamed)'
                md.append(f'{i}. **{name}**')
                if s.get('summary'):
                    md.append(f'   - {s["summary"][:150]}...')
            md.append('')
        md.append('')
    
    # ==========================================================================
    # 4. ALL RELATIONSHIP TYPES
    # ==========================================================================
    md.append('---')
    md.append('')
    md.append('## 4. Relationship Types')
    md.append('')
    
    # Neo4j relationship types
    rel_types = run_query(session, '''
        MATCH ()-[r]->()
        RETURN type(r) as t, count(*) as c
        ORDER BY c DESC
    ''')
    
    md.append('### 4.1. Neo4j Relationship Types')
    md.append('')
    md.append('| Type | Count |')
    md.append('|------|-------|')
    for r in rel_types:
        md.append(f'| `{r["t"]}` | {r["c"]:,} |')
    md.append('')
    
    # ALL semantic edge types (r.name)
    edge_types = run_query(session, '''
        MATCH ()-[r:RELATES_TO]->()
        RETURN r.name as edge, count(*) as c
        ORDER BY c DESC
    ''')
    
    md.append('### 4.2. ALL Semantic Edge Types (RELATES_TO.name)')
    md.append('')
    md.append(f'**Total Unique Edge Types: {len(edge_types)}**')
    md.append('')
    md.append('| Edge Type | Count |')
    md.append('|-----------|-------|')
    for r in edge_types:  # Show ALL edge types
        md.append(f'| `{r["edge"]}` | {r["c"]} |')
    md.append('')
    
    # ==========================================================================
    # 5. RELATIONSHIP PATTERNS
    # ==========================================================================
    md.append('---')
    md.append('')
    md.append('## 5. Relationship Patterns')
    md.append('')
    md.append('Common patterns showing (FromType)--[EDGE]-->(ToType)')
    md.append('')
    md.append('| From | Edge | To | Count |')
    md.append('|------|------|----|-------|')
    
    patterns = run_query(session, '''
        MATCH (a)-[r:RELATES_TO]->(b)
        WITH labels(a)[0] as from_type, r.name as edge, labels(b)[0] as to_type, count(*) as cnt
        WHERE cnt >= 5
        RETURN from_type, edge, to_type, cnt
        ORDER BY cnt DESC
        LIMIT 100
    ''')
    
    for p in patterns:
        md.append(f'| {p["from_type"]} | `{p["edge"]}` | {p["to_type"]} | {p["cnt"]} |')
    md.append('')
    
    # ==========================================================================
    # 6. ORPHAN NODES
    # ==========================================================================
    md.append('---')
    md.append('')
    md.append('## 6. Orphan Nodes (No RELATES_TO connections)')
    md.append('')
    
    orphans = run_query(session, '''
        MATCH (n)
        WHERE NOT (n)-[:RELATES_TO]-() AND NOT (n)<-[:RELATES_TO]-()
          AND NOT n:Episodic
        RETURN labels(n)[0] as label, n.name as name
        ORDER BY labels(n)[0], n.name
    ''')
    
    md.append(f'**Total Orphan Nodes: {len(orphans)}**')
    md.append('')
    
    # Group by label
    orphan_groups = {}
    for o in orphans:
        label = o['label']
        if label not in orphan_groups:
            orphan_groups[label] = []
        orphan_groups[label].append(o['name'])
    
    for label, names in orphan_groups.items():
        md.append(f'### {label} ({len(names)} orphans)')
        md.append('')
        for name in names:
            md.append(f'- {name if name else "(unnamed)"}')
        md.append('')
    
    # ==========================================================================
    # 7. DATA QUALITY METRICS
    # ==========================================================================
    md.append('---')
    md.append('')
    md.append('## 7. Data Quality Metrics')
    md.append('')
    
    # Nodes with null names
    null_names = run_query(session, '''
        MATCH (n)
        WHERE n.name IS NULL AND NOT n:Episodic
        RETURN labels(n)[0] as label, count(*) as cnt
    ''')
    
    md.append('### Nodes with NULL names')
    md.append('')
    if null_names:
        md.append('| Label | Count |')
        md.append('|-------|-------|')
        for r in null_names:
            md.append(f'| {r["label"]} | {r["cnt"]} |')
    else:
        md.append('None')
    md.append('')
    
    # Duplicate names
    duplicates = run_query(session, '''
        MATCH (n)
        WHERE n.name IS NOT NULL
        WITH n.name as name, collect(n) as nodes, count(*) as cnt
        WHERE cnt > 1
        RETURN name, cnt
        ORDER BY cnt DESC
        LIMIT 30
    ''')
    
    md.append('### Duplicate Entity Names (Top 30)')
    md.append('')
    if duplicates:
        md.append('| Name | Count |')
        md.append('|------|-------|')
        for d in duplicates:
            md.append(f'| {d["name"][:50]} | {d["cnt"]} |')
    else:
        md.append('None')
    md.append('')
    
    # ==========================================================================
    # 8. QUERY EXAMPLES
    # ==========================================================================
    md.append('---')
    md.append('')
    md.append('## 8. Query Examples')
    md.append('')
    
    queries = [
        ('Find all zones in Austin', '''MATCH (j:Jurisdiction)-[r:RELATES_TO]->(z:Zone)
WHERE r.name = 'CONTAINS' AND j.name CONTAINS 'Austin'
RETURN z.name, z.code, z.family
ORDER BY z.name'''),
        ('Find zones that allow townhouses', '''MATCH (z:Zone)-[r:RELATES_TO]->(u:UseType)
WHERE r.name = 'ALLOWS_USE' AND u.name CONTAINS 'Townhouse'
RETURN z.name, u.name'''),
        ('Get constraints for a zone', '''MATCH (z:Zone)-[:RELATES_TO]-(r:Rule)-[rel:RELATES_TO]->(c:Constraint)
WHERE z.name CONTAINS 'SF-5' AND rel.name = 'HAS_CONSTRAINT'
RETURN z.name, r.name, c.name, c.summary'''),
        ('Find all state overrides', '''MATCH (o:Override)
RETURN o.name, o.bill_id, o.metric, o.override_value, o.summary'''),
        ('Trace rule to source document', '''MATCH (r:Rule)-[rel:RELATES_TO]->(d:DocumentSource)
WHERE rel.name = 'SOURCED_FROM'
RETURN r.name, r.section, d.document, d.section
LIMIT 10'''),
        ('Find orphan nodes', '''MATCH (n)
WHERE NOT (n)-[:RELATES_TO]-() AND NOT (n)<-[:RELATES_TO]-()
  AND NOT n:Episodic
RETURN labels(n) as type, n.name as name'''),
        ('Get all edge types', '''MATCH ()-[r:RELATES_TO]->()
RETURN DISTINCT r.name as edge_type, count(*) as count
ORDER BY count DESC'''),
        ('Full hierarchy visualization', '''MATCH path = (j:Jurisdiction)-[:RELATES_TO*1..4]->(n)
WHERE j.name CONTAINS 'Austin'
RETURN path
LIMIT 200'''),
    ]
    
    for title, query in queries:
        md.append(f'### {title}')
        md.append('```cypher')
        md.append(query)
        md.append('```')
        md.append('')
    
    # ==========================================================================
    # 9. ONTOLOGY SUMMARY
    # ==========================================================================
    md.append('---')
    md.append('')
    md.append('## 9. Ontology Summary')
    md.append('')
    md.append('### Entity Hierarchy')
    md.append('```')
    md.append('Jurisdiction (city, county, state)')
    md.append('├── Zone (zoning districts: SF-1 to SF-6, MF-1 to MF-6, CBD, etc.)')
    md.append('│   └── UseType (permitted uses: residential, commercial, mixed)')
    md.append('│       └── Rule (LDC regulations)')
    md.append('│           └── Constraint (quantitative limits)')
    md.append('│               └── Condition (contextual triggers)')
    md.append('└── Override (state preemptions: SB-840, SB-2835)')
    md.append('    └── supersedes local Constraints')
    md.append('')
    md.append('DocumentSource: Citations linked to all entity types via SOURCED_FROM')
    md.append('Entity: Untyped entities extracted by LLM (need classification)')
    md.append('Episodic: Source text episodes (306 ingested)')
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
    md.append('* --[MENTIONS]--> * (Episodic connections)')
    md.append('```')
    md.append('')
    
    # ==========================================================================
    # 10. DATA SOURCES
    # ==========================================================================
    md.append('---')
    md.append('')
    md.append('## 10. Data Sources')
    md.append('')
    md.append('| Source | Description |')
    md.append('|--------|-------------|')
    md.append('| Austin LDC | Land Development Code (~103,756 lines, 3.35M chars) |')
    md.append('| Texas SB-840 | Housing in commercial areas (density, height, setbacks) |')
    md.append('| Texas SB-2835 | Transit-oriented development (density, parking) |')
    md.append('')
    
    md.append('---')
    md.append('')
    md.append('*End of Knowledge Graph Documentation*')
    
    return '\n'.join(md)


def main():
    with driver.session() as session:
        print('Generating comprehensive zoning_kg.md from Neo4j...')
        md_content = generate_markdown(session)
        with open('zoning_kg.md', 'w') as f:
            f.write(md_content)
        print(f'  Saved zoning_kg.md ({len(md_content):,} bytes)')
        
        # Count lines
        lines = md_content.count('\n')
        print(f'  Lines: {lines}')
    
    driver.close()
    print('Done!')


if __name__ == '__main__':
    main()
