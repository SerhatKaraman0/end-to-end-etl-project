## ETL Pipeline Project

End-to-end ETL pipeline for a network security dataset. The pipeline ingests data from MongoDB, validates and checks for drift, transforms features with a Sklearn pipeline, and writes versioned artifacts.

### Architecture
- **Entry point**: `main.py`
- **Components**:
  - `etl_project/components/data_ingestion.py`
  - `etl_project/components/data_validation.py`
  - `etl_project/components/data_transformation.py`
- **Config and entities**:
  - `etl_project/entity/config_entity.py` (paths and hyperparameters)
  - `etl_project/entity/artifact_entity.py` (typed artifacts)
- **Utilities**: `etl_project/utils/main_utils/utils.py`
- **Constants**: `etl_project/constants/training_pipeline/__init__.py`
- **Exceptions**: `etl_project/exception/exception.py`

Artifacts are written under `artifacts/<MM_DD_YYYY_HH_MM_SS>/...` for each run.

### Requirements
- Python 3.11
- MongoDB instance accessible via a URI

Install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

Key dependency pins:
- `pymongo>=4.6,<5` (Python 3.11 compatible)

### Configuration
Provide your MongoDB URI in a `.env` file at the project root:
```env
MONGO_DB_URI=mongodb+srv://<user>:<password>@<cluster>/<db>?retryWrites=true&w=majority
```

The dataset schema path is controlled by `SCHEMA_FILE_PATH` in `etl_project/constants/training_pipeline/__init__.py`.

### Running the pipeline
```bash
python main.py
```

On success, you will see printed artifacts for ingestion, validation, and transformation, for example:
```text
DataIngestionArtifact(...)
DataValidationArtifact(...)
DataTransformationArtifact(...)
```

### Outputs and artifact layout
- `artifacts/<ts>/data_ingestion/feature_store/phisingData.csv`
- `artifacts/<ts>/data_ingestion/ingested/{train.csv,test.csv}`
- `artifacts/<ts>/data_validation/{train.csv,test.csv}`
- `artifacts/<ts>/data_validation/drift_report/report.yaml`
- `artifacts/<ts>/data_transformation/transformed/{train.npy,test.npy}`
- `artifacts/<ts>/data_transformation/transformed_object/preprocessing.pkl`

### Important modules and functions

#### Data ingestion (`etl_project/components/data_ingestion.py`)
- `DataIngestion.export_collection_as_df()`
  - Connects to MongoDB via `pymongo.MongoClient(MONGO_DB_URI)` and loads a collection to a `pandas.DataFrame`.
  - Drops the `"_id"` column if present.
- `DataIngestion.export_data_into_feature_store(df)`
  - Writes the raw dataframe to the feature store CSV file path from `DataIngestionConfig.feature_store_dir`.
- `DataIngestion.split_data_as_train_test_set(df)`
  - Splits the dataframe using `train_test_split` with ratio from constants.
  - Writes `train.csv` and `test.csv` under the ingested directory.
- `DataIngestion.initiate_data_ingestion()`
  - Orchestrates the steps above and returns `DataIngestionArtifact` with train/test file paths.

#### Data validation (`etl_project/components/data_validation.py`)
- `DataValidation.validate_num_of_cols(df)`
  - Compares dataframe column count to the schema (length of the loaded YAML).
- `DataValidation.detect_data_drift(base_df, current_df, threshold=0.05)`
  - Uses `scipy.stats.ks_2samp` on each column; flags drift if p-value < threshold.
  - Writes a YAML drift report to `data_validation/drift_report/report.yaml`.
  - Returns a boolean `status` indicating whether distributions are the same across all columns.
- `DataValidation.initiate_data_validation()`
  - Reads validated train/test from ingestion outputs, runs schema checks and drift detection.
  - Writes validated `train.csv`/`test.csv` and returns `DataValidationArtifact`.

#### Data transformation (`etl_project/components/data_transformation.py`)
- `DataTransformation.get_data_transformer_object()`
  - Builds a `sklearn.pipeline.Pipeline` with a `KNNImputer` using `DATA_TRANSFORMATION_IMPUTER_PARAMS`.
- `DataTransformation.initiate_data_transformation()`
  - Loads validated CSVs, splits into input/target using `TARGET_COLUMN`.
  - Fits the imputer pipeline on train inputs; transforms train/test.
  - Persists arrays to `.npy` files and the pipeline to `preprocessing.pkl`.
  - Returns `DataTransformationArtifact` with file paths.

#### Configs (`etl_project/entity/config_entity.py`)
- `TrainingPipelineConfig` sets the timestamped `artifacts/<ts>` root.
- `DataIngestionConfig` sets feature store and ingested file paths.
- `DataValidationConfig` sets validated/invalid directories and drift report path.
- `DataTransformationConfig` sets transformed arrays and preprocessing object paths.

#### Exceptions (`etl_project/exception/exception.py`)
- `ETLPipelineException` wraps errors with file and line information.
- Robust to cases where it is raised outside an active exception context.

#### Utilities (`etl_project/utils/main_utils/utils.py`)
- `read_yaml_file(path)` and `write_yaml_file(path, content)`
- `save_numpy_array_data(path, array)` and `save_object(path, obj)` for artifacts.

### Troubleshooting
- ImportError about `collections.MutableMapping`:
  - Ensure `pymongo>=4.6,<5` is installed; run `pip install -r requirements.txt`.
- Drift report file cannot be written:
  - Confirm parent directory exists; current implementation ensures it with `os.makedirs(os.path.dirname(path), exist_ok=True)`.
- MongoDB connection issues:
  - Verify `MONGO_DB_URI` in `.env` and that your IP is allowed in the cluster.

### Development notes
- Artifacts are versioned by timestamp; re-running the pipeline creates a new directory under `artifacts/`.
- Constants live in `etl_project/constants/training_pipeline/__init__.py` to centralize names and hyperparameters.


# Trigger deployment
