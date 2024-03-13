#!/bin/bash -eux
ls -al requirements
for req in requirements/*.in; do
  uv pip compile --generate-hashes --allow-unsafe --quiet --upgrade --strip-extras --resolver=backtracking $req --output-file=${req%.*}.txt
done
