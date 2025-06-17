---
sidebar_position: 1
---

# Basic Usage Examples

This guide provides basic examples of using CerebroMCP for common tasks. These examples demonstrate the core functionality and best practices for working with the framework.

## Setting Up the Client

First, let's set up the MCP client with proper configuration:

```python
from cerebromcp import MCPClient

client = MCPClient(
    api_key="your_api_key",
    config={
        "max_retries": 3,
        "timeout": 30,
        "log_level": "INFO"
    }
)
```

## Registering Models

Register available models with their capabilities:

```python
from cerebromcp import ModelRegistry

registry = ModelRegistry()

# Register GPT-4
registry.register_model(
    name="gpt-4",
    capabilities=["text-generation", "code-completion"],
    max_tokens=8192
)

# Register a custom model
registry.register_model(
    name="custom-model",
    capabilities=["custom-task"],
    max_tokens=4096
)
```

## Basic Task Execution

Execute a simple text generation task:

```python
from cerebromcp import TaskOrchestrator

orchestrator = TaskOrchestrator(registry)

# Simple text generation
result = orchestrator.execute_task(
    task_type="text-generation",
    input_data={
        "prompt": "Write a short story about a robot",
        "max_tokens": 100
    }
)

print(result.output)
```

## Managing Context

Handle conversation context:

```python
from cerebromcp import ContextManager

context_manager = ContextManager()

# Add context to a conversation
context_manager.add_context(
    conversation_id="conv_123",
    context={
        "user_input": "Tell me about AI",
        "timestamp": "2024-03-20T10:00:00Z"
    }
)

# Retrieve context
context = context_manager.get_context("conv_123")
```

## Error Handling

Implement proper error handling:

```python
from cerebromcp import MCPError

try:
    result = orchestrator.execute_task(
        task_type="text-generation",
        input_data={"prompt": "Hello"}
    )
except MCPError as e:
    print(f"Error occurred: {e.message}")
    print(f"Status code: {e.status_code}")
    # Handle the error appropriately
```

## Complete Example

Here's a complete example that combines all the above concepts:

```python
from cerebromcp import MCPClient, ModelRegistry, TaskOrchestrator, ContextManager

def main():
    # Initialize components
    client = MCPClient(api_key="your_api_key")
    registry = ModelRegistry()
    orchestrator = TaskOrchestrator(registry)
    context_manager = ContextManager()

    # Register models
    registry.register_model(
        name="gpt-4",
        capabilities=["text-generation"],
        max_tokens=8192
    )

    # Create a conversation
    conversation_id = "conv_123"
    context_manager.add_context(
        conversation_id=conversation_id,
        context={"user_input": "Initial message"}
    )

    try:
        # Execute task
        result = orchestrator.execute_task(
            task_type="text-generation",
            input_data={
                "prompt": "Write a poem about programming",
                "max_tokens": 200
            }
        )

        # Update context with result
        context_manager.add_context(
            conversation_id=conversation_id,
            context={"model_output": result.output}
        )

        print("Generated poem:", result.output)

    except MCPError as e:
        print(f"Error: {e.message}")

if __name__ == "__main__":
    main()
```

## Next Steps

- Explore [Advanced Workflows](../examples/advanced-workflows)
- Learn about [Best Practices](../best-practices/model-selection)
- Check out the [API Reference](../api/overview) 