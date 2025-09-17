// components/Register.jsx
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function Register() {
  const navigate = useNavigate()

  return (
    <div className="form-container">
      <h1>Register</h1>
      <Formik
        initialValues={{ email: '', username: '', password: '' }}
        validationSchema={Yup.object({
          email: Yup.string().email('Invalid email').required('Required'),
          username: Yup.string().required('Required'),
          password: Yup.string().min(6, 'Minimum 6 characters').required('Required'),
        })}
        onSubmit={async (values, { setSubmitting, setFieldError }) => {
          try {
            await axios.post('http://localhost:5555/api/auth/register', values)
            navigate('/login')
          } catch (err) {
            setFieldError('email', 'User already exists or invalid input')
          } finally {
            setSubmitting(false)
          }
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <div>
              <label>Email</label>
              <Field name="email" type="email" />
              <ErrorMessage name="email" component="div" />
            </div>
            <div>
              <label>Username</label>
              <Field name="username" type="text" />
              <ErrorMessage name="username" component="div" />
            </div>
            <div>
              <label>Password</label>
              <Field name="password" type="password" />
              <ErrorMessage name="password" component="div" />
            </div>
            <button type="submit" disabled={isSubmitting}>
              Register
            </button>
          </Form>
        )}
      </Formik>
    </div>
  )
}
