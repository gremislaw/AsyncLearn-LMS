import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Layout, Menu, Button, message, Spin } from 'antd';
import { HomeOutlined, BookOutlined, UserOutlined, LoginOutlined, LogoutOutlined } from '@ant-design/icons';
import axios from 'axios';

// Компоненты страниц
import Dashboard from './pages/Dashboard';
import Courses from './pages/Courses';
import CourseDetail from './pages/CourseDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import AdminPanel from './pages/AdminPanel';

const { Header, Content, Footer } = Layout;

const App = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  // Проверка авторизации при загрузке
  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          const response = await axios.get('/users/me');
          setUser(response.data);
        } catch (error) {
          console.error('Ошибка авторизации:', error);
          localStorage.removeItem('token');
          setToken(null);
          delete axios.defaults.headers.common['Authorization'];
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, [token]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
    message.success('Вы вышли из системы');
  };

  // Меню навигации
  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: 'Главная',
    },
    {
      key: '/courses',
      icon: <BookOutlined />,
      label: 'Курсы',
    },
  ];

  // Добавляем пункт меню для админа
  if (user && user.role === 'admin') {
    menuItems.push({
      key: '/admin',
      icon: <UserOutlined />,
      label: 'Админ-панель',
    });
  }

  return (
    <Router>
      <Layout className="layout" style={{ minHeight: '100vh' }}>
        <Header>
          <div className="logo" style={{ float: 'left', width: '120px', height: '31px', margin: '16px 24px 16px 0', background: 'rgba(255, 255, 255, 0.3)' }} />
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['/']}
            items={menuItems}
            style={{ lineHeight: '64px' }}
            onClick={({ key }) => {
              window.location.href = key;
            }}
          />
          <div style={{ float: 'right' }}>
            {user ? (
              <div style={{ color: 'white', marginRight: '20px' }}>
                <span>{user.username}</span>
                <Button
                  type="primary"
                  icon={<LogoutOutlined />}
                  onClick={handleLogout}
                  style={{ marginLeft: '10px' }}
                >
                  Выйти
                </Button>
              </div>
            ) : (
              <Button
                type="primary"
                icon={<LoginOutlined />}
                onClick={() => window.location.href = '/login'}
              >
                Войти
              </Button>
            )}
          </div>
        </Header>
        <Content style={{ padding: '0 50px' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '50px' }}>
              <Spin size="large" />
            </div>
          ) : (
            <Routes>
              <Route path="/" element={<Dashboard user={user} />} />
              <Route path="/courses" element={<Courses user={user} />} />
              <Route path="/courses/:id" element={<CourseDetail user={user} />} />
              <Route path="/login" element={user ? <Navigate to="/" /> : <Login setToken={setToken} setUser={setUser} />} />
              <Route path="/register" element={user ? <Navigate to="/" /> : <Register />} />
              {user && user.role === 'admin' && (
                <Route path="/admin" element={<AdminPanel user={user} />} />
              )}
            </Routes>
          )}
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          AsyncLearn LMS ©2023 Created with FastAPI & React
        </Footer>
      </Layout>
    </Router>
  );
};

export default App;
