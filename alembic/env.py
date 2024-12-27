from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Base  # Импортируем Base из моделей
from app.database import DATABASE_URL  # Подключаем строку подключения из конфигурации

# Эта строка указывает на настройки логирования
if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

# target_metadata указывает на метаданные вашей базы данных для миграций
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в режиме 'offline'."""
    url = DATABASE_URL  # Строка подключения к базе данных
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Запуск миграций в режиме 'online'."""
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Запуск миграции в зависимости от режима
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()