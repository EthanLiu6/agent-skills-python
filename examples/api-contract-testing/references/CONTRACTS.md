# Contracts Overview

## Endpoint: POST /v1/orders

- Request required fields: `order_id`, `items`, `currency`
- Response required fields: `order_id`, `status`, `created_at`
- Backward compatibility rule: avoid removing or retyping existing fields
