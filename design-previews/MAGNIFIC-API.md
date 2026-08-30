# Magnific Nano Banana Pro API workflow

Verified against the current official Magnific API documentation on 2026-08-30.

- Base URL: `https://api.magnific.com`
- Authentication: `x-magnific-api-key` request header
- Create: `POST /v1/ai/text-to-image/nano-banana-pro`
- Poll: `GET /v1/ai/text-to-image/nano-banana-pro/{task-id}`
- Requested preview settings: `aspect_ratio: "16:9"`, `resolution: "1K"`
- Required field: `prompt` with 2 to 3,000 characters
- Optional references: up to 14 public PNG, JPEG, or WebP images
- Successful create response: task object with `task_id`, `status`, and initially empty `generated`
- Completion response: `status: "COMPLETED"` and one or more generated image URLs

Official sources:

- [Magnific API documentation index](https://docs.magnific.com/llms.txt)
- [Nano Banana Pro create endpoint](https://docs.magnific.com/api-reference/text-to-image/post-nano-banana-pro.md)
- [Nano Banana Pro task list endpoint](https://docs.magnific.com/api-reference/text-to-image/get-nano-banana-pro.md)

Credential handling rule: the API key must be injected into a single process as an ephemeral environment variable, must not appear in command arguments or output, and must never be written to this repository.
