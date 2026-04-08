mkdir -p src/components
mkdir -p src/utils
mkdir -p data/raw
mkdir -p data/processed
mkdir -p vectorstore
mkdir -p research

touch src/__init__.py
touch src/components/loader.py
touch src/components/splitter.py
touch src/components/embedding.py
touch src/components/retriever.py
touch src/components/rag_chain.py

touch src/utils/helper.py
touch src/utils/prompt.py

touch app.py
touch config.py
touch .env
touch setup.py
touch requirements.txt

touch research/trials.ipynb

touch src/components/pipeline.py
touch src/utils/logger.py
touch src/utils/exceptions.py

echo "Structure Ready"