# SQL-Challenge
# SQL 15 Days Challenge

A comprehensive 15-day SQL challenge implementation using Python and SQLite, featuring various data analysis problems and solutions.

## 🎯 Overview

This project contains 15 different SQL challenges that cover a wide range of database operations and data analysis scenarios. Each challenge includes problem statements, synthetic data generation, and optimized SQL solutions.

## 🚀 Features

- **15 SQL Challenges** - From basic queries to complex data analysis
- **SQLite Integration** - Lightweight, serverless database
- **Synthetic Data** - Auto-generated test data for each challenge
- **Utility Functions** - Helper functions for database operations
- **Modern Python** - Built with Python 3.13+
- **UV Package Manager** - Fast dependency management

## 📋 Prerequisites

- Python 3.12 or higher
- UV package manager (recommended) or pip

## 🛠️ Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/ehsankf/SQL-Challenge.git
cd SQL-Challenge/src

# Install dependencies
uv sync
```

# SQL 15 Days Challenge

A comprehensive 15-day SQL challenge implementation using Python and SQLite, featuring various data analysis problems and solutions.

## 🎯 Overview

This project contains 15 different SQL challenges that cover a wide range of database operations and data analysis scenarios. Each challenge includes problem statements, synthetic data generation, and optimized SQL solutions.

## 🚀 Features

- **15 SQL Challenges** - From basic queries to complex data analysis
- **SQLite Integration** - Lightweight, serverless database
- **Synthetic Data** - Auto-generated test data for each challenge
- **Utility Functions** - Helper functions for database operations
- **Modern Python** - Built with Python 3.12+
- **UV Package Manager** - Fast dependency management

## 📋 Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

## 🛠️ Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/ehsankf/SQL-Challenge.git
cd SQL-Challenge/src

# Install dependencies
uv sync
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/ehsankf/SQL-Challenge.git
cd SQL-Challenge/src

# Install the project
pip install -e .
```

## 🎮 Usage

### Run Individual Challenges

```bash
# Using UV
uv run python sql_1.py
uv run python sql_2.py
# ... etc

# Using the script entry point
uv run sql-challenge

# Using pip
python sql_1.py
python main.py
```


## 📚 Challenge Overview

| Day | Challenge | Description |
|-----|-----------|-------------|
| 1 | User Engagement Analysis | Calculate percentage of users who never liked or commented |
| 2 | Order Pattern Analysis | Analyze user ordering patterns (home vs other addresses) |
| 3 | Job Posting Patterns | Count job posting patterns by users |
| 4-6 | Various SQL Operations | Complex joins, aggregations, and data transformations |
| 7 | Upselling Analysis | Find customers upsold with additional products |
| 8-11 | Advanced Queries | Window functions, CTEs, and complex filtering |
| 12 | Streak Analysis | Calculate longest continuous streaks of platform visits |
| 13-15 | Final Challenges | Complex data analysis and reporting |

## 🔧 Development

### Project Structure

```
src/
├── main.py              # Entry point
├── utils.py             # Database utility functions
├── sql_1.py - sql_15.py # Individual challenge solutions
├── pyproject.toml       # Project configuration
├── README.md           # This file
└── sql_challenge.db    # Generated SQLite database
```

## 🛠️ Utility Functions

The `utils.py` module provides helpful database operations:

- `delete_table(conn, table_name)` - Drop tables safely
- `list_tables(conn)` - List all database tables
- `list_table_cols(conn, table_name)` - Show table schema
- `add_column(conn, table_name, col_name, col_type)` - Add columns
- `select_data(conn, query)` - Execute SELECT queries

## 📖 Example Challenge

```python
# sql_1.py - User Engagement Analysis
"""
Find the percentage of users who have never liked or commented on any posts.
"""

# Create tables with synthetic data
cursor.execute('''CREATE TABLE users (user_id INTEGER, name TEXT)''')
cursor.execute('''CREATE TABLE likes (user_id INTEGER, post_id INTEGER)''')
cursor.execute('''CREATE TABLE comments (user_id INTEGER, post_id INTEGER)''')

# SQL Solution
query = '''
WITH engaged_users AS (
    SELECT DISTINCT user_id FROM likes
    UNION
    SELECT DISTINCT user_id FROM comments
)
SELECT 
    ROUND(
        (COUNT(*) - (SELECT COUNT(*) FROM engaged_users)) * 100.0 / COUNT(*), 2
    ) as percentage_never_engaged
FROM users;
'''
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-challenge`)
3. Commit your changes (`git commit -am 'Add new SQL challenge'`)
4. Push to the branch (`git push origin feature/new-challenge`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Ehsan Kazemi**
- LinkedIn: [ehsan-kazemi](https://www.linkedin.com/in/ehsan-kazemi/)
- GitHub: [ehsankf](https://github.com/ehsankf)

## 🌟 Acknowledgments

- Inspired by real-world data analysis scenarios
- Built for learning and practicing SQL skills
- Designed for both beginners and advanced users

---
