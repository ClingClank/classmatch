const LS = {
  get: (k) => JSON.parse(localStorage.getItem(k) || 'null'),
  set: (k, v) => localStorage.setItem(k, JSON.stringify(v))
}

export function signup({ email, password, name, prefs }) {
  const users = LS.get('users') || []
  if (users.find(u => u.email === email)) throw new Error('Email exists')
  users.push({ email, password, name, prefs })
  LS.set('users', users)
  return true
}

export function login({ email, password }) {
  const users = LS.get('users') || []
  const u = users.find(u => u.email === email && u.password === password)
  if (!u) throw new Error('Invalid credentials')
  LS.set('session', { email })
  return { email }
}

export function me() {
  return LS.get('session')
}

export function logout() {
  localStorage.removeItem('session')
}

export function coursesOf(email) {
  const store = LS.get('courses') || {}
  return store[email] || []
}

export function setCourses(email, list) {
  const store = LS.get('courses') || {}
  store[email] = list
  LS.set('courses', store)
}

export function matches(email, filters = {}) {
  const users = LS.get('users') || []
  return users.filter(u => u.email !== email).slice(0, 5)
}

export function createGroup(email, payload) {
  const gs = LS.get('groups') || []
  const id = 'g' + (gs.length + 1)
  gs.push({ id, owner: email, ...payload })
  LS.set('groups', gs)
  return id
}

export function myGroups(email) {
  const gs = LS.get('groups') || []
  return gs.filter(g => g.owner === email).slice(0, 5)
}
