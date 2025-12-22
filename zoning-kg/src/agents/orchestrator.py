"""Pipeline orchestrator with beautiful verbose output."""

import json
from dataclasses import dataclass
from typing import Optional
from .analyst import ZoningAnalyst
from .formatter import ResponseFormatter
from .schemas import ZoningResponse


# ASCII Art and formatting
BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ██████╗ ██████╗  ██████╗  █████╗ ███╗   ██╗██╗███████╗███╗   ███╗       ║
║    ██╔═══██╗██╔══██╗██╔════╝ ██╔══██╗████╗  ██║██║╚══███╔╝████╗ ████║       ║
║    ██║   ██║██████╔╝██║  ███╗███████║██╔██╗ ██║██║  ███╔╝ ██╔████╔██║       ║
║    ██║   ██║██╔══██╗██║   ██║██╔══██║██║╚██╗██║██║ ███╔╝  ██║╚██╔╝██║       ║
║    ╚██████╔╝██║  ██║╚██████╔╝██║  ██║██║ ╚████║██║███████╗██║ ╚═╝ ██║       ║
║     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝     ╚═╝       ║
║                                                                              ║
║                    🏗️  Zoning Knowledge Graph Agent  🏗️                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

STEP_DIVIDER = "─" * 80

def box_text(title: str, content: str, width: int = 78) -> str:
    """Create a boxed text section."""
    lines = []
    lines.append(f"┌{'─' * (width - 2)}┐")
    lines.append(f"│ {title.center(width - 4)} │")
    lines.append(f"├{'─' * (width - 2)}┤")
    
    for line in content.split('\n'):
        # Truncate long lines
        if len(line) > width - 4:
            line = line[:width - 7] + "..."
        lines.append(f"│ {line.ljust(width - 4)} │")
    
    lines.append(f"└{'─' * (width - 2)}┘")
    return '\n'.join(lines)


def step_header(step_num: int, title: str, icon: str = "🔹") -> str:
    """Create a step header."""
    return f"""
{STEP_DIVIDER}
  {icon}  STEP {step_num}: {title}
{STEP_DIVIDER}"""


def success_box(message: str) -> str:
    """Create a success message box."""
    return f"""
    ╭────────────────────────────────────────────────────────────╮
    │  ✅  {message.ljust(54)} │
    ╰────────────────────────────────────────────────────────────╯"""


def error_box(message: str) -> str:
    """Create an error message box."""
    return f"""
    ╭────────────────────────────────────────────────────────────╮
    │  ❌  {message[:54].ljust(54)} │
    ╰────────────────────────────────────────────────────────────╯"""


def info_line(label: str, value: str, icon: str = "→") -> str:
    """Create an info line."""
    return f"    {icon} {label}: {value}"


@dataclass
class PipelineResult:
    """Result from the agent pipeline."""
    success: bool
    response: Optional[ZoningResponse]
    raw_response: Optional[dict]
    analysis: Optional[str]
    graph_context: Optional[str]
    error: Optional[str]


class ZoningQueryPipeline:
    """Orchestrates the agent pipeline for zoning queries.
    
    Pipeline flow:
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │  User Question  │ -> │ Text-to-Cypher  │ -> │  Execute Query  │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                                          │
                                                          ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │  JSON Response  │ <- │ Formatter Agent │ <- │  Analyst Agent  │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
    """
    
    def __init__(self, verbose: bool = False, max_retries: int = 3):
        """Initialize the pipeline.
        
        Args:
            verbose: If True, print intermediate steps with beautiful formatting
            max_retries: Maximum retry attempts for text-to-cypher
        """
        self.verbose = verbose
        self.max_retries = max_retries
        self.analyst = ZoningAnalyst(verbose=verbose, max_retries=max_retries)
        self.formatter = ResponseFormatter()
    
    def _print(self, *args, **kwargs):
        """Print only if verbose mode is enabled."""
        if self.verbose:
            print(*args, **kwargs)
    
    def query(self, question: str) -> PipelineResult:
        """Process a zoning question through the full pipeline.
        
        Args:
            question: Natural language zoning question
            
        Returns:
            PipelineResult with response or error
        """
        try:
            # Banner
            if self.verbose:
                print(BANNER)
                print(f"\n  📋 QUERY: \"{question}\"\n")
            
            # Step 1: Get graph context
            self._print(step_header(1, "TEXT-TO-CYPHER & GRAPH RETRIEVAL", "🔍"))
            self._print("\n  Converting natural language to Cypher and querying Neo4j...")
            self._print(f"  Max retries: {self.max_retries}")
            
            graph_context = self.analyst.get_graph_context(question)
            context_len = len(graph_context)
            
            self._print(success_box(f"Graph context retrieved ({context_len} chars)"))
            
            # Step 2: Run analyst agent
            self._print(step_header(2, "ZONING ANALYST AGENT", "🧠"))
            self._print("\n  Analyzing zoning data with domain expertise...")
            self._print(info_line("Model", self.analyst.config.model))
            self._print(info_line("Temperature", str(self.analyst.config.temperature)))
            
            analysis = self.analyst.analyze(question, graph_context)
            
            self._print(success_box(f"Analysis complete ({len(analysis)} chars)"))
            
            if self.verbose:
                print("\n  📝 ANALYST OUTPUT:")
                print("  " + "─" * 60)
                # Indent and truncate analysis for display
                for line in analysis.split('\n')[:30]:
                    print(f"  │ {line[:75]}")
                if len(analysis.split('\n')) > 30:
                    print(f"  │ ... ({len(analysis.split(chr(10))) - 30} more lines)")
                print("  " + "─" * 60)
            
            # Step 3: Run formatter agent
            self._print(step_header(3, "RESPONSE FORMATTER AGENT", "📦"))
            self._print("\n  Converting analysis to structured JSON...")
            
            try:
                response = self.formatter.format(question, analysis)
                
                self._print(success_box("JSON validation passed"))
                
                if self.verbose:
                    print("\n  📊 FINAL RESPONSE:")
                    print("  " + "─" * 60)
                    json_str = response.model_dump_json(indent=2)
                    for line in json_str.split('\n')[:40]:
                        print(f"  │ {line}")
                    if len(json_str.split('\n')) > 40:
                        print(f"  │ ... (truncated)")
                    print("  " + "─" * 60)
                
                # Summary
                if self.verbose:
                    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              📊 RESULT SUMMARY                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Permitted:    {str(response.permitted).ljust(62)}║
║  Confidence:   {response.confidence.ljust(62)}║
║  Constraints:  {str(len(response.constraints)).ljust(62)}║
║  Overrides:    {str(len(response.overrides)).ljust(62)}║
║  Conditions:   {str(len(response.conditions)).ljust(62)}║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
                
                return PipelineResult(
                    success=True,
                    response=response,
                    raw_response=response.model_dump(),
                    analysis=analysis,
                    graph_context=graph_context,
                    error=None
                )
                
            except ValueError as e:
                self._print(error_box(f"Validation failed: {str(e)[:40]}"))
                
                raw = self.formatter.format_raw(question, analysis)
                return PipelineResult(
                    success=False,
                    response=None,
                    raw_response=raw,
                    analysis=analysis,
                    graph_context=graph_context,
                    error=str(e)
                )
                
        except Exception as e:
            self._print(error_box(f"Pipeline error: {str(e)[:40]}"))
            
            if self.verbose:
                import traceback
                traceback.print_exc()
            
            return PipelineResult(
                success=False,
                response=None,
                raw_response=None,
                analysis=None,
                graph_context=None,
                error=str(e)
            )
    
    def query_json(self, question: str) -> str:
        """Process a query and return JSON string.
        
        Args:
            question: Natural language zoning question
            
        Returns:
            JSON string of the response
        """
        result = self.query(question)
        
        if result.success and result.response:
            return result.response.model_dump_json(indent=2)
        elif result.raw_response:
            return json.dumps(result.raw_response, indent=2)
        else:
            return json.dumps({
                "error": result.error,
                "success": False
            }, indent=2)
