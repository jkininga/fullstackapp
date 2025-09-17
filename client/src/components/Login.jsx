// components/Login.jsx
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const navigate = useNavigate()

  return (
    <div className="form-container">
      <h1>Login</h1>
      <Formik
        initialValues={{ email: '', password: '' }}
        validationSchema={Yup.object({
          email: Yup.string().email('Invalid email').required('Required'),
          password: Yup.string().required('Required'),
        })}
        onSubmit={async (values, { setSubmitting, setFieldError }) => {
          try {
            const res = await axios.post('http://localhost:5555/api/auth/login', values)
            localStorage.setItem('token', res.data.access_token)
            navigate('/projects')
          } catch (err) {
            setFieldError('email', 'Invalid credentials')
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
              <label>Password</label>
              <Field name="password" type="password" />
              <ErrorMessage name="password" component="div" />
            </div>
            <button type="submit" disabled={isSubmitting}>
              Login
            </button>
          </Form>
        )}
      </Formik>
    </div>
  )
}

