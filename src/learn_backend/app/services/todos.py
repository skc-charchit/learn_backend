from sqlalchemy.orm import Session

from learn_backend.app.models.todo import Todo
from learn_backend.app.schemas.todos import TodoCreate, TodoUpdate


def create_todo(session: Session, todo: TodoCreate) -> Todo:
    # create a new todo item
    todo_item = Todo(**todo.model_dump())
    session.add(todo_item)
    session.commit()
    session.refresh(todo_item)
    return todo_item


def get_todo(session: Session, todo_id: int) -> Todo | None:
    # get a todo item by id
    # instead of
    #   `session.query(Todo).filter(Todo.id == todo_id).first()`,
    # we use
    #   `session.get(Todo, todo_id)`
    # which is more efficient and cleaner.
    #   - Cleaner
    #   - Faster
    #   - Primary-key optimized
    #   - More modern (SQLAlchemy 1.4+ / 2.0 style)

    todo_item = session.get(Todo, todo_id)
    return todo_item


def update_todo(session: Session, todo_id: int, todo: TodoUpdate) -> Todo | None:
    # update a todo item by id
    todo_item = session.get(Todo, todo_id)

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(todo_item, key, value)

    session.commit()
    session.refresh(todo_item)
    return todo_item


def delete_todo(session: Session, todo_id: int) -> bool:
    # delete a todo item by id
    todo_item = session.get(Todo, todo_id)
    if not todo_item:
        return False

    session.delete(todo_item)
    session.commit()
    return True
