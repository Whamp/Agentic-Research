# MCP Code Execution Framework

This project is a Python-based implementation of the "MCP-as-code" concept, as described in the Anthropic blog post [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp).

## Summary

The core idea of this framework is to enable AI agents to interact with MCP (Model Context Protocol) servers more efficiently by writing and executing code, rather than making direct tool calls. This approach offers several advantages:

- **Context Efficiency:** Agents can dynamically discover and load only the tool definitions they need for a given task, significantly reducing the number of tokens required.
- **Improved Data Handling:** Large datasets can be processed and filtered within the execution environment, with only the relevant results being passed back to the model.
- **State Persistence:** Agents can save intermediate results to a file-based workspace, allowing them to resume complex tasks and track progress.
- **Skill Creation:** Agents can save generated code as reusable "skills," enabling them to build a library of higher-level capabilities over time.

## Architecture

The framework consists of the following components:

- **`client.py`:** A mock MCP client that simulates calls to MCP servers.
- **`servers/`:** A directory containing mock MCP server implementations (e.g., `google_drive`, `salesforce`) as Python packages. Each tool is represented by a Python file.
- **`agent_simulation.py`:** A script that simulates an agent's workflow, demonstrating tool discovery, code generation, and execution.
- **`workspace/`:** A directory where the agent can store intermediate results.
- **`skills/`:** A directory where the agent can save and reuse generated code as skills.

## How to Run the Simulation

To run the agent simulation, execute the following command from the root of the repository:

```bash
python -m mcp_code_execution.agent_simulation
```

The script will output a detailed log of the agent's simulated thought process and actions.
