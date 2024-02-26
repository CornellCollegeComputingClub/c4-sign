lint:
    autoflake --in-place -r c4_sign --remove-all-unused-imports --remove-unused-variables
    isort c4_sign --py 39
    black -t py39 c4_sign -l 120
