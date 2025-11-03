import Login from './pages/Login'
import Signup from './pages/Signup'
import Matches from './pages/Matches'
import CreateGroup from './pages/CreateGroup'
import Dashboard from './pages/Dashboard'

export default [
  { path: '/', element: Login },
  { path: '/signup', element: Signup },
  { path: '/matches', element: Matches },
  { path: '/create-group', element: CreateGroup },
  { path: '/dashboard', element: Dashboard }
]
