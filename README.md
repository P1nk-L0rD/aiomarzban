# aiomarzban

Async SDK for the Marzban API based on aiohttp, requests, and pydantic. This library is fully compatible with **Marzban version 0.8.4** and supports all panel methods.

## Features

- Async library for non-blocking operations
- Automatic under-the-hood access token management
- All functions implemented as native class methods
- Extensive test coverage for most of the code
- Default values can be provided for user creation
- Simplified user creation through method parameters
- Automatic conversion of gigabytes to bytes
- Custom methods for tailored functionality


## Installation

```bash
pip install aiomarzban
```


## Examples


## Test coverage

**Warning**: It is highly not recommended to run tests on a production server!

- [x] Admin
- [x] Core
- [x] Node
- [ ] Subscription
- [x] System
- [x] User template
- [x] User

To run tests:

Create .env file with panel information

```bash
pytest tests/
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Run tests to ensure everything works (optional).
5. Submit a pull request.

## Tasks

1. Fix tests to avoid timeouts
2. Tests for subscription
3. ~~Timeout for requests~~
4. ~~Retries for requests~~
5. More custom useful methods

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, suggestions, or feedback, please reach out to [my telegram](https://t.me/IMC_tech).
