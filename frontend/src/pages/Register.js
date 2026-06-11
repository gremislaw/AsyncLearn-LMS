import React, { useState } from 'react';
import { Card, Form, Input, Button, Typography, message, Select } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Paragraph } = Typography;
const { Option } = Select;

const Register = () => {
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      await axios.post('/auth/register', {
        username: values.username,
        email: values.email,
        password: values.password,
        role: values.role || 'student'
      });

      message.success('Регистрация прошла успешно! Теперь вы можете войти в систему.');
      window.location.href = '/login';
    } catch (error) {
      message.error('Ошибка при регистрации. Возможно, пользователь с таким именем или email уже существует.');
      console.error('Ошибка при регистрации:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
      <Card style={{ width: '400px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <Title level={2}>Регистрация</Title>
          <Paragraph>AsyncLearn LMS</Paragraph>
        </div>
        <Form
          name="register"
          onFinish={onFinish}
          autoComplete="off"
        >
          <Form.Item
            name="username"
            rules={[
              { required: true, message: 'Пожалуйста, введите имя пользователя!' },
              { min: 3, message: 'Имя пользователя должно содержать минимум 3 символа!' }
            ]}
          >
            <Input 
              prefix={<UserOutlined />} 
              placeholder="Имя пользователя" 
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="email"
            rules={[
              { required: true, message: 'Пожалуйста, введите email!' },
              { type: 'email', message: 'Пожалуйста, введите корректный email!' }
            ]}
          >
            <Input 
              prefix={<MailOutlined />} 
              placeholder="Email" 
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              { required: true, message: 'Пожалуйста, введите пароль!' },
              { min: 6, message: 'Пароль должен содержать минимум 6 символов!' }
            ]}
          >
            <Input.Password 
              prefix={<LockOutlined />} 
              placeholder="Пароль" 
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="confirmPassword"
            dependencies={['password']}
            rules={[
              { required: true, message: 'Пожалуйста, подтвердите пароль!' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('Введенные пароли не совпадают!'));
                },
              }),
            ]}
          >
            <Input.Password 
              prefix={<LockOutlined />} 
              placeholder="Подтвердите пароль" 
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="role"
            initialValue="student"
          >
            <Select size="large" placeholder="Выберите роль">
              <Option value="student">Студент</Option>
              <Option value="admin">Администратор</Option>
            </Select>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block size="large" loading={loading}>
              Зарегистрироваться
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            <Paragraph>
              Уже есть аккаунт? <a href="/login">Войти</a>
            </Paragraph>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default Register;
