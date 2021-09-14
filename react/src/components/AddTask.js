import { useState } from 'react'

const AddTask = ({ onAdd }) => {
  let [age, setage] = useState('')
  let [name, setname] = useState('')
  let [lastname, setlastname] = useState('')
  let [sex, setsex] = useState('')


  const onSubmit = (e) => {
    e.preventDefault()

    if (!age || !name|| !lastname || !sex) {
      console.log("using default vals");

      age = 19
      name = 'Blanduzia';
      sex = 'female';
      lastname = 'Pascali';
 
      // alert('Please fill all fields')
      // return
    }

    onAdd({ age, name, lastname, sex })

    setage('')
    setname('')
    setlastname('')
    setsex('')

  }

  return (
    <form className='add-form' onSubmit={onSubmit}>
      <div className='form-control'>
        <label>Age</label>
        <input
          type='text'
          placeholder='add age'
          value={age}
          onChange={(e) => setage(e.target.value)}
        />
      </div>
      <div className='form-control'>
        <label>Name</label>
        <input
          type='text'
          placeholder='add name'
          value={name}
          onChange={(e) => setname(e.target.value)}
        />
      </div>
      <div className='form-control'>
        <label>Last name</label>
        <input
          type='text'
          placeholder='Add last name'
          value={lastname}
          onChange={(e) => setlastname(e.target.value)}
        />
      </div>
      <div className='form-control'>
        <label>Sex</label>
        <input
          type='text'
          placeholder='male/female'
          value={sex}
          onChange={(e) => setsex(e.target.value)}
        />
      </div>
      <input type='submit' value='Save Task' className='btn btn-block' />
    </form>
  )
}

export default AddTask
