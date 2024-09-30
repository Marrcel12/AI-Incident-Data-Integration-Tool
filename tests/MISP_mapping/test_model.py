import numpy
import pytest
from unittest.mock import patch, MagicMock
from MISP_mapping.model.model import encode_text, get_example_texts, cluster_to_topic, get_topic_for_row

@pytest.fixture
def mock_tokenizer_model():
    with patch('MISP_mapping.model.model.AutoTokenizer.from_pretrained') as mock_tokenizer, \
         patch('MISP_mapping.model.model.AutoModel.from_pretrained') as mock_model:
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()
        mock_model.return_value(**{"return_tensors": 'pt', "padding": True, "truncation": True, "max_length": 512}) \
            .return_value.pooler_output.detach().numpy.return_value.flatten.return_value = [0.5, -0.5]
        yield mock_tokenizer, mock_model

@pytest.fixture
def mock_kmeans():
    with patch('MISP_mapping.model.model.KMeans') as mock:
        instance = mock.return_value
        instance.fit.return_value = instance
        instance.predict.return_value = [0]
        yield instance

@pytest.fixture
def mock_get_texts():
    with patch('MISP_mapping.model.model.get_example_texts_with_topics') as mock:
        mock.return_value = [("Example text", "Topic1"), ("Another example", "Topic2")]
        yield mock

def test_encode_text(mock_tokenizer_model):
    text = "Test input text"
    result = encode_text(text)
    assert isinstance(result, numpy.ndarray)  

def test_get_example_texts(mock_get_texts):
    texts = get_example_texts()
    assert texts == ["Example text", "Another example"]

def test_cluster_to_topic(mock_get_texts):
    assert cluster_to_topic(0) == "Topic1"
    assert cluster_to_topic(1) == "Topic2"
    assert cluster_to_topic(99) == "Unknown"

def test_get_topic_for_row(mock_tokenizer_model, mock_kmeans, mock_get_texts):
    assert get_topic_for_row("Test input text") == "Topic1"