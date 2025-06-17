---
sidebar_position: 1
---

# API Overview

The CerebroMCP API provides a comprehensive set of tools for managing AI models, orchestrating tasks, and handling context. This section provides an overview of the main components and their interactions.

## Core Components

### MCPClient

The main entry point for interacting with the CerebroMCP system.

```python
from cerebromcp import MCPClient

client = MCPClient(
    api_key="your_api_key",
    config={
        "max_retries": 3,
        "timeout": 30
    }
)
```

### ModelRegistry

Manages the registration and discovery of AI models.

```python
from cerebromcp import ModelRegistry

registry = ModelRegistry()
registry.register_model(
    name="gpt-4",
    capabilities=["text-generation"],
    max_tokens=8192
)
```

### TaskOrchestrator

Coordinates the execution of tasks across multiple models.

```python
from cerebromcp import TaskOrchestrator

orchestrator = TaskOrchestrator(registry)
result = orchestrator.execute_task(
    task_type="text-generation",
    input_data={"prompt": "Hello, world!"}
)
```

### ContextManager

Handles conversation history and context management.

```python
from cerebromcp import ContextManager

context_manager = ContextManager()
context_manager.add_context(
    conversation_id="conv_123",
    context={"user_input": "Previous message"}
)
```

## API Structure

The API is organized into several key modules:

1. **Models**: Model registration and management
2. **Tasks**: Task definition and execution
3. **Context**: Context management and history
4. **Protocol**: Communication protocol handling

## Authentication

All API requests require authentication using an API key:

```python
client = MCPClient(api_key="your_api_key")
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error messages:

```python
try:
    result = client.process_request("Your request")
except MCPError as e:
    print(f"Error: {e.message}")
    print(f"Status code: {e.status_code}")
```

## Rate Limiting

API requests are subject to rate limiting. The current limits are:

- 100 requests per minute for standard plans
- 1000 requests per minute for enterprise plans

## Versioning

The API is versioned using semantic versioning. The current version is 1.0.0.

## Next Steps

- Explore the [Models API](../api/models)
- Learn about [Task Management](../api/tasks)
- Understand [Context Management](../api/context) 