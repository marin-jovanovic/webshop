import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import Tasks from './components/Tasks'
import AddTask from './components/AddTask'
import About from './components/About'

const crypto = require('crypto')

const App = () => {
  const [showAddTask, setShowAddTask] = useState(false)
  const [tasks, setTasks] = useState([])

  useEffect(() => {
    const getTasks = async () => {
      // const tasksFromServer = await fetchTasks()
      setTasks({})
    }

    getTasks()
  }, [])
  
  // Delete Task
  const deleteTask = async (id) => {
    const res = await fetch(`http://localhost:5000/tasks/${id}`, {
      method: 'DELETE',
    })
    //We should control the response status to decide if we will change the state or not.
    res.status === 200
      ? setTasks(tasks.filter((task) => task.id !== id))
      : alert('Error Deleting This product, please refresh website')
  }

  // Add Task
  const addTask = async (task) => {

    console.log('task data', task);
    console.log(task["age"]);

    let age = task["age"];
    let sex = task["sex"];
    let name = task["name"];
    let lastname = task["lastname"];

    let payload = `[${age}, '${name}', '${sex}', '${lastname}']`
    
    let hash = crypto.createHash('md5').update(payload).digest("hex");

    console.log("hash", hash)
 
//    hash = "bbde768edffe850af38746488c9664b9"

    const res = await fetch(`http://localhost:8000/api/users/${hash}`, {
      mode: 'cors'
    })

    console.log("res", res);
    const data = await res.json()

    console.log("data", data);

    let user_id = data.data.user_id

    console.log("user id", user_id)

    let t = await fetch(`http://localhost:8000/api/reccom/${user_id}`, {
      mode: 'cors'
    })

    t = (await t.json()).data

    console.log('r', t)

    let r = [
      t.l_1,
      t.l_2,
      t.l_3,
      t.l_4,
      t.l_5,
      t.l_6,
      t.l_7,
      t.l_8,
      t.l_9,
      t.l_10,
    ]

    console.log("r", r)

    let result = []

    for (const iterator of r) {
      t = await fetch(`http://localhost:8000/api/prod/${iterator}`, {
        mode: 'cors'
      })

      t = (await t.json()).data.product

      console.log('t', t)

      result.push(t);

    }

    console.log("result", result)

    let f = [];
    let i = 0;

    result.forEach(e => {

      f.push({
        "id": i+1,
        "text": e,        
      })

      i++;
    })

    setTasks(f);

  }

  return (
    <Router>
      <div className='container'>

        <Header
          onAdd={() => setShowAddTask(!showAddTask)}
          showAdd={showAddTask}
        />
        <Route
          path='/'
          exact
          render={(props) => (
            <>
              {showAddTask && <AddTask onAdd={addTask} />}
              {tasks.length > 0 ? (
                <Tasks
                  tasks={tasks}
                  onDelete={deleteTask}
                  // onToggle={toggleReminder}
                />
              ) : (
                'No Products To Show'
              )}
            </>
          )}
        />
        <Route path='/about' component={About} />
        <Footer />
      </div>
    </Router>
  )
}

export default App
