if [ "${PRODUCTION}" = "false" ]; then
	# find ./ -name "test_*.py" -not -path "./venv/*" | xargs pytest -s -v &&
	uvicorn main:app --host ${SERVER_HOST} --port ${SERVER_PORT} --reload
else
	uvicorn main:app --host ${SERVER_HOST} --port ${SERVER_PORT}
fi