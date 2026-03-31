import { useState, useEffect, useCallback } from 'react';
import { taskAPI, userAPI, Task, User, isConflictError, getConflictData } from './api';
import './App.css';

type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE';

interface LocalTask extends Task {
  isLoading?: boolean;
}

export default function App() {
  const [tasks, setTasks] = useState<LocalTask[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [message, setMessage] = useState<{ type: 'error' | 'success'; text: string } | null>(null);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newUserName, setNewUserName] = useState('');
  const [editingTask, setEditingTask] = useState<LocalTask | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editStatus, setEditStatus] = useState<TaskStatus>('TODO');
  const [editAssignedTo, setEditAssignedTo] = useState<string>('');

  // Fetch tasks
  const fetchTasks = useCallback(async () => {
    try {
      const response = await taskAPI.getAll();
      setTasks(response.data);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    }
  }, []);

  // Fetch users
  const fetchUsers = useCallback(async () => {
    try {
      const response = await userAPI.getAll();
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users:', error);
    }
  }, []);

  // Initial load
  useEffect(() => {
    fetchTasks();
    fetchUsers();
  }, [fetchTasks, fetchUsers]);

  // Polling sync every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchTasks();
    }, 3000);

    return () => clearInterval(interval);
  }, [fetchTasks]);

  // Create user
  const handleCreateUser = async () => {
    if (!newUserName.trim()) return;

    try {
      await userAPI.create(newUserName);
      setNewUserName('');
      await fetchUsers();
      showMessage('User created successfully', 'success');
    } catch (error) {
      console.error('Create user error:', error);
      showMessage('Failed to create user', 'error');
    }
  };

  // Create task
  const handleCreateTask = async () => {
    if (!newTaskTitle.trim()) return;

    try {
      await taskAPI.create(newTaskTitle);
      setNewTaskTitle('');
      await fetchTasks();
      showMessage('Task created successfully', 'success');
    } catch (error) {
      console.error('Create task error:', error);
      showMessage('Failed to create task', 'error');
    }
  };

  // Update task
  const handleUpdateTask = async () => {
    if (!editingTask) return;

    setTasks((prev) =>
      prev.map((t) =>
        t.id === editingTask.id ? { ...t, isLoading: true } : t
      )
    );

    try {
      const response = await taskAPI.update(
        editingTask.id,
        editTitle !== editingTask.title ? editTitle : undefined,
        editStatus !== editingTask.status ? editStatus : undefined,
        editAssignedTo !== (editingTask.assigned_to || '') ? (editAssignedTo || null) : undefined,
        editingTask.version
      );

      setTasks((prev) =>
        prev.map((t) =>
          t.id === editingTask.id ? { ...response.data, isLoading: false } : t
        )
      );

      setEditingTask(null);
      showMessage('Task updated successfully', 'success');
    } catch (error) {
      if (isConflictError(error)) {
        const conflictData = getConflictData(error);
        if (conflictData) {
          // Revert to latest data
          setTasks((prev) =>
            prev.map((t) =>
              t.id === editingTask.id
                ? { ...conflictData.latest_task, isLoading: false }
                : t
            )
          );
          showMessage('Conflict detected: Task was modified. Reverted to latest version.', 'error');
          setEditingTask(null);
        }
      } else {
        showMessage('Failed to update task', 'error');
        setTasks((prev) =>
          prev.map((t) =>
            t.id === editingTask.id ? { ...t, isLoading: false } : t
          )
        );
      }
    }
  };

  // Delete task
  const handleDeleteTask = async (id: string) => {
    setTasks((prev) =>
      prev.map((t) =>
        t.id === id ? { ...t, isLoading: true } : t
      )
    );

    try {
      await taskAPI.delete(id);
      setTasks((prev) => prev.filter((t) => t.id !== id));
      showMessage('Task deleted successfully', 'success');
    } catch (error) {
      showMessage('Failed to delete task', 'error');
      setTasks((prev) =>
        prev.map((t) =>
          t.id === id ? { ...t, isLoading: false } : t
        )
      );
    }
  };

  // Open edit modal
  const openEditModal = (task: LocalTask) => {
    setEditingTask(task);
    setEditTitle(task.title);
    setEditStatus(task.status);
    setEditAssignedTo(task.assigned_to || '');
  };

  // Close edit modal
  const closeEditModal = () => {
    setEditingTask(null);
  };

  // Show message
  const showMessage = (text: string, type: 'error' | 'success') => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 4000);
  };

  // Group tasks by status
  const tasksByStatus = {
    TODO: tasks.filter((t) => t.status === 'TODO'),
    IN_PROGRESS: tasks.filter((t) => t.status === 'IN_PROGRESS'),
    DONE: tasks.filter((t) => t.status === 'DONE'),
  };

  // Format timestamp to local time
  const formatTimestamp = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
    });
  };

  // Render task card
  const renderTaskCard = (task: LocalTask) => {
    const assignedUser = users.find((u) => u.id === task.assigned_to);

    return (
      <div key={task.id} className={`task-card ${task.isLoading ? 'loading' : ''}`}>
        <div className="task-title">{task.title}</div>
        <div className="task-meta">
          <span>v{task.version}</span>
          <span>{formatTimestamp(task.updated_at)}</span>
        </div>
        {assignedUser && <div className="task-assigned">{assignedUser.name}</div>}
        <div className="task-actions">
          <button onClick={() => openEditModal(task)} disabled={task.isLoading}>
            Edit
          </button>
          <button
            className="delete"
            onClick={() => handleDeleteTask(task.id)}
            disabled={task.isLoading}
          >
            Delete
          </button>
        </div>
      </div>
    );
  };

  // Render column
  const renderColumn = (status: TaskStatus, label: string) => {
    const columnTasks = tasksByStatus[status];

    return (
      <div key={status} className="column">
        <div className={`column-header ${status.toLowerCase().replace('_', '-')}`}>
          <span>{label}</span>
          <span className="task-count">{columnTasks.length}</span>
        </div>
        <div className="tasks-container">
          {columnTasks.length === 0 ? (
            <div className="loading">No tasks</div>
          ) : (
            columnTasks.map(renderTaskCard)
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="app">
      <div className="header">
        <h1>Collaborative Task Board</h1>

        {message && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}

        <div className="header-actions">
          <div className="input-group">
            <input
              type="text"
              placeholder="New user name..."
              value={newUserName}
              onChange={(e) => setNewUserName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleCreateUser()}
            />
            <button onClick={handleCreateUser}>Add User</button>
          </div>

          <div className="input-group">
            <input
              type="text"
              placeholder="New task title..."
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleCreateTask()}
            />
            <button onClick={handleCreateTask}>Add Task</button>
          </div>
        </div>
      </div>

      <div className="board">
        {renderColumn('TODO', 'To Do')}
        {renderColumn('IN_PROGRESS', 'In Progress')}
        {renderColumn('DONE', 'Done')}
      </div>

      {editingTask && (
        <div className="modal open">
          <div className="modal-content">
            <div className="modal-header">Edit Task</div>
            <div className="modal-body">
              <input
                type="text"
                placeholder="Task title"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
              />
              <select value={editStatus} onChange={(e) => setEditStatus(e.target.value as TaskStatus)}>
                <option value="TODO">To Do</option>
                <option value="IN_PROGRESS">In Progress</option>
                <option value="DONE">Done</option>
              </select>
              <select value={editAssignedTo} onChange={(e) => setEditAssignedTo(e.target.value)}>
                <option value="">Unassigned</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="modal-footer">
              <button className="cancel" onClick={closeEditModal}>
                Cancel
              </button>
              <button onClick={handleUpdateTask}>Save</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
