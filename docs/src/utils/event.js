export const handlers = {}

export const on = (event, handler) => {
    if (!handlers[event]) {
        handlers[event] = [];
    }
    handlers[event].push(handler);
}

export const emit = (event, ...args) => {
    if (handlers[event]) {
        handlers[event].forEach(handler => handler(...args));
    }
}