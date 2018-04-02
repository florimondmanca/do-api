"""Route configuration."""

import resources


routes = {
    '/lists': resources.ListResource(),
    '/lists/{id:int}': resources.ListDetailResource(),
    '/tasks/': resources.TaskResource(),
    '/tasks/{id:int}': resources.TaskDetailResource(),
}
