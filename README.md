# AI Incident Data Integration Tool

This tool is designed to facilitate the effective sharing and processing of AI-related incident data from the AIAAIC repository to the MISP (Malware Information Sharing Platform) for enhanced cybersecurity measures. It enables the rapid and machine-readable distribution of incident data, assisting in the rapid response to AI-related security threats.

## Setup

### Requirements

- Python 3.x
- Docker (running MISP in a container)

### Installation

1. **Virtual Environment:**

   To create and activate the virtual environment:

   ```bash
   make activate-venv
   ```

2. **Dependencies:**

   To install required Python packages:

   ```bash
   make install
   ```

### Configuration

- **MISP Object Template:**

  Before running the tool, ensure the AI incident object template is uploaded to your MISP instance. This can be done using:

  ```bash
  make upload_config
  ```

  Replace `YOUR_SRC` with the path to your local `definition.json` and `ad7be4fd1e32` with your MISP Docker container ID.

## Usage

The tool provides several Make commands to manage the data integration process:

- **Get Data:**

  To fetch data from the AIAAIC via Google Sheets:

  ```bash
  make get-data
  ```

- **Map Data:**

  To map the fetched data to the MISP format:

  ```bash
  make map-data
  ```

- **Direct Processing:**

  To directly process and create MISP events:

  ```bash
  make direct-process
  ```

- **Run Script:**

  To execute the main script that processes and creates MISP events:

  ```bash
  make run-script
  ```

- **Testing and Linting:**

  Run tests and lint the code:

  ```bash
  make run-tests
  make lint
  ```

## Additional Tools

- **Performance Monitoring:**

  To evaluate the performance of the data processing:

  ```bash
  make performance
  ```

This tool is part of a broader effort to adapt cybersecurity practices to the challenges posed by AI technologies, enhancing threat intelligence and incident response capabilities.
