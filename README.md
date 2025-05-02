# aurora-iam-db

[![PyPI](https://img.shields.io/pypi/v/aurora-iam-db.svg)](https://pypi.org/project/aurora-iam-db/)
[![GitHub](https://img.shields.io/github/license/YOUR_USERNAME/aurora-iam-db)](https://github.com/YOUR_USERNAME/aurora-iam-db)
[![CI](https://github.com/YOUR_USERNAME/aurora-iam-db/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/aurora-iam-db/actions)

A lightweight Python utility for securely connecting to **Amazon Aurora MySQL** using **IAM authentication**, supporting:

✅ SQLAlchemy-based connection pooling  
✅ Async support via `aiomysql`  
✅ Retry logic on failures  
✅ AWS IRSA- and EKS-friendly  
✅ No passwords or secrets in code

---

## 🚀 Installation

```bash
pip install aurora-iam-db
```

Or from GitHub Packages:

```bash
pip install --extra-index-url https://__token__:<GITHUB_TOKEN>@pip.pkg.github.com/YOUR_USERNAME aurora-iam-db
```

---

## 🔧 Use Cases

- Secure backend services running on **EKS**
- Replaces hardcoded RDS passwords with **IAM authentication**
- Easily pluggable into async and sync workflows

---

## 🧠 Quick Examples

### Synchronous (SQLAlchemy)

```python
from aurora_iam_db import AuroraIAMDatabase
from sqlalchemy import text

db = AuroraIAMDatabase(
    db_host="my-cluster.cluster-xyz.us-east-1.rds.amazonaws.com",
    db_name="mydb",
    db_user="my_iam_user",
    region="us-east-1",
    ssl_ca_path="/app/rds-combined-ca-bundle.pem"
)

result = db.execute_query(text("SELECT NOW();"))
print(result)
```

### Asynchronous (aiomysql)

```python
import asyncio
from aurora_iam_db import AsyncAuroraIAMDatabase

async def run():
    db = AsyncAuroraIAMDatabase(
        db_host="my-cluster.cluster.amazonaws.com",
        db_name="mydb",
        db_user="my_iam_user",
        region="us-east-1",
        ssl_ca_path="/app/rds-combined-ca-bundle.pem"
    )
    result = await db.execute_query("SELECT NOW();")
    print(result)

asyncio.run(run())
```

---

## ⚙️ Configuration

| Parameter         | Type    | Default | Description                                                                 |
|------------------|---------|---------|-----------------------------------------------------------------------------|
| `db_host`        | `str`   | —       | Endpoint of your Aurora MySQL cluster                                      |
| `db_name`        | `str`   | —       | Database name to connect to                                                |
| `db_user`        | `str`   | —       | IAM database user name                                                     |
| `region`         | `str`   | —       | AWS region (e.g., `us-east-1`)                                             |
| `ssl_ca_path`    | `str`   | (req'd) | Path to the RDS combined CA bundle `.pem` file                             |
| `pool_size`      | `int`   | `10`    | Max Size of the SQLAlchemy connection pool                                     |
| `max_overflow`   | `int`   | `5`     | Number of extra connections beyond `pool_size`                             |
| `pool_recycle`   | `int`   | `900`   | Seconds before recycling a connection (token expires after 15 min)         |
| `pool_timeout`   | `int`   | `30`    | Max wait time (in seconds) for a pooled connection                         |
| `retry_attempts` | `int`   | `3`     | Number of times to retry on connection failures                            |
| `retry_delay`    | `int`   | `2`     | Delay (in seconds) between retry attempts                                  |

---

## 🛡️ Security Best Practices

- Use [IAM DB Auth](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
- Mount [RDS SSL Cert](https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem) to container
- Use [IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) to avoid AWS access keys

---

## 🧪 Running Tests

```bash
pytest
```

Unit tests mock out AWS calls and validate token generation logic.

---

## 📦 Publishing

To release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

CI will auto-publish to **PyPI** and **GitHub Packages** using GitHub Actions.

---

## 📄 License

[MIT](LICENSE)

---

## 🧩 Related AWS Resources

- [IAM DB Authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
- [Connecting securely with IAM tokens](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.html)
- [SSL certificate downloads](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html)