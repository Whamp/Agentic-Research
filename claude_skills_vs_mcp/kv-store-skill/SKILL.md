---
name: kv-store-skill
description: A skill for interacting with a simple key-value store. Use this skill to get, set, and delete values from the store.
---

# Key-Value Store Skill

This skill allows you to interact with a simple key-value store. You can use the provided scripts to perform the following operations:

## Get a value

To get a value from the store, use the `get.py` script with the desired key as an argument:

```bash
python scripts/get.py <key>
```

## Set a value

To set a value in the store, use the `set.py` script with the key and value as arguments:

```bash
python scripts/set.py <key> <value>
```

## Delete a value

To delete a value from the store, use the `delete.py` script with the key as an argument:

```bash
python scripts/delete.py <key>
```
