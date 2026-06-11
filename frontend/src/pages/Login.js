import React, { useState } from 'react';
import { Card, Form, Input, Button, Typography, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Paragraph } = Typography;

const Login = ({ setToken, setUser }) => {
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const response = await axios.post('/auth/login', {
        username: values.username,
        password: values.password
      });

      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      setToken(access_token);

      // Получаем информацию о пользователе
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      const userResponse = await axios.get('/users/me');
      setUser(userResponse.data);

      message.success('Вы успешно вошли в систему!');
      window.location.href = '/';
    } catch (error) {
      message.error('Ошибка при входе. Проверьте имя пользователя и пароль.');
      console.error('Ошибка при входе:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#f0f2f5' }}>
      <Card style={{ width: '400px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <Title level={2}>Вход в систему</Title>
          <Paragraph>AsyncLearn LMS</Paragraph>
        </div>
        <Form
          name="login"
          onFinish={onFinish}
          autoComplete="off"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: 'Пожалуйста, введите имя пользователя!' }]}
          >
            <Input 
              prefix={<UserOutlined />} 
              placeholder="Имя пользователя" 
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Пожалуйста, введите пароль!' }]}
          >
            <Input.Password 
              prefix={<LockOutlined />} 
              placeholder="Пароль" 
              size="large"
            />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block size="large" loading={loading}>
              Войти
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            <Paragraph>
              Нет аккаунта? <a href="/register">Зарегистрироваться</a>
            </Paragraph>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default Login;
