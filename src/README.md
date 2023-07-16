## Setup & Installation

- See README.md in root directory

## Project Structure

- `config.py`: App Configuration
- `mock_data`: Mock Data for Testing
- `parameters`: Custom Arcpy Parameter Modules
- `platform_api`: Services for accessing Ursa Platform Endpoints
- `tools`: Arcpy Tools loaded into ArcGIS Python Toolbox
- `utils`: Shared utilities and helpers

## Tests

- To run all tests, execute `test_runner.py` using python executable from ArcGIS Pro Conda Environment. Requires ArcPy. Test modules use the `*_test.py` pattern.
- Ex: `C:/Users/<username>/AppData/Local/ESRI/conda/envs/arcgispro-py3-clone/python.exe c:/Users/<username>/dev/ursa-arcgis-toolbox/src/test_runner.py`
