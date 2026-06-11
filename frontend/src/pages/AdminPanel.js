import React, { useState, useEffect } from 'react';
import { Card, Tabs, Table, Button, Upload, message, Typography, Tag, Space, Modal, Form, Input, InputNumber } from 'antd';
import { UploadOutlined, PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title } = Typography;
const { TabPane } = Tabs;

const AdminPanel = ({ user }) => {
  const [courses, setCourses] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isCourseModalVisible, setIsCourseModalVisible] = useState(false);
  const [isUserModalVisible, setIsUserModalVisible] = useState(false);
  const [courseForm] = Form.useForm();
  const [userForm] = Form.useForm();
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [coursesResponse, usersResponse] = await Promise.all([
        axios.get('/courses'),
        axios.get('/admin/users')
      ]);
      setCourses(coursesResponse.data);
      setUsers(usersResponse.data);
    } catch (error) {
      message.error('Ошибка при загрузке данных');
      console.error('Ошибка при загрузке данных:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCourse = async (values) => {
    try {
      await axios.post('/courses', values);
      message.success('Курс успешно создан!');
      setIsCourseModalVisible(false);
      courseForm.resetFields();
      fetchData();
    } catch (error) {
      message.error('Ошибка при создании курса');
      console.error('Ошибка при создании курса:', error);
    }
  };

  const handleUpdateCourse = async (values) => {
    try {
      await axios.put(`/admin/courses/${selectedCourse.id}`, values);
      message.success('Курс успешно обновлен!');
      setIsCourseModalVisible(false);
      courseForm.resetFields();
      setSelectedCourse(null);
      fetchData();
    } catch (error) {
      message.error('Ошибка при обновлении курса');
      console.error('Ошибка при обновлении курса:', error);
    }
  };

  const handleDeleteCourse = async (courseId) => {
    try {
      await axios.delete(`/admin/courses/${courseId}`);
      message.success('Курс успешно удален!');
      fetchData();
    } catch (error) {
      message.error('Ошибка при удалении курса');
      console.error('Ошибка при удалении курса:', error);
    }
  };

  const handleCreateUser = async (values) => {
    try {
      await axios.post('/admin/users', values);
      message.success('Пользователь успешно создан!');
      setIsUserModalVisible(false);
      userForm.resetFields();
      fetchData();
    } catch (error) {
      message.error('Ошибка при создании пользователя');
      console.error('Ошибка при создании пользователя:', error);
    }
  };

  const handleUpdateUser = async (values) => {
    try {
      await axios.put(`/admin/users/${selectedUser.id}`, values);
      message.success('Пользователь успешно обновлен!');
      setIsUserModalVisible(false);
      userForm.resetFields();
      setSelectedUser(null);
      fetchData();
    } catch (error) {
      message.error('Ошибка при обновлении пользователя');
      console.error('Ошибка при обновлении пользователя:', error);
    }
  };

  const handleDeleteUser = async (userId) => {
    try {
      await axios.delete(`/admin/users/${userId}`);
      message.success('Пользователь успешно удален!');
      fetchData();
    } catch (error) {
      message.error('Ошибка при удалении пользователя');
      console.error('Ошибка при удалении пользователя:', error);
    }
  };

  const handleUploadVideo = async (info) => {
    if (info.file.status === 'done') {
      message.success('Видео успешно загружено!');
    } else if (info.file.status === 'error') {
      message.error('Ошибка при загрузке видео');
    }
  };

  const uploadProps = {
    name: 'file',
    action: '/admin/upload-video',
    headers: {
      authorization: `Bearer ${localStorage.getItem('token')}`,
    },
    onChange: handleUploadVideo,
  };

  const courseColumns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Название',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: 'Цена',
      dataIndex: 'price',
      key: 'price',
      render: (price) => `${price} ₽`,
    },
    {
      title: 'Статус',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (isActive) => (
        <Tag color={isActive ? 'green' : 'red'}>
          {isActive ? 'Активен' : 'Неактивен'}
        </Tag>
      ),
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button
            type="primary"
            icon={<EditOutlined />}
            size="small"
            onClick={() => {
              setSelectedCourse(record);
              courseForm.setFieldsValue(record);
              setIsCourseModalVisible(true);
            }}
          >
            Редактировать
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            size="small"
            onClick={() => handleDeleteCourse(record.id)}
          >
            Удалить
          </Button>
        </Space>
      ),
    },
  ];

  const userColumns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Имя пользователя',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Роль',
      dataIndex: 'role',
      key: 'role',
      render: (role) => (
        <Tag color={role === 'admin' ? 'red' : 'blue'}>
          {role === 'admin' ? 'Администратор' : 'Студент'}
        </Tag>
      ),
    },
    {
      title: 'Статус',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (isActive) => (
        <Tag color={isActive ? 'green' : 'red'}>
          {isActive ? 'Активен' : 'Неактивен'}
        </Tag>
      ),
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button
            type="primary"
            icon={<EditOutlined />}
            size="small"
            onClick={() => {
              setSelectedUser(record);
              userForm.setFieldsValue(record);
              setIsUserModalVisible(true);
            }}
          >
            Редактировать
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            size="small"
            onClick={() => handleDeleteUser(record.id)}
          >
            Удалить
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: '20px 0' }}>
      <Title level={2}>Админ-панель</Title>
      <Tabs defaultActiveKey="courses">
        <TabPane tab="Курсы" key="courses">
          <Card
            title="Управление курсами"
            extra={
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => setIsCourseModalVisible(true)}
              >
                Создать курс
              </Button>
            }
          >
            <Table
              columns={courseColumns}
              dataSource={courses}
              loading={loading}
              rowKey="id"
            />
          </Card>
        </TabPane>

        <TabPane tab="Пользователи" key="users">
          <Card
            title="Управление пользователями"
            extra={
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => setIsUserModalVisible(true)}
              >
                Создать пользователя
              </Button>
            }
          >
            <Table
              columns={userColumns}
              dataSource={users}
              loading={loading}
              rowKey="id"
            />
          </Card>
        </TabPane>

        <TabPane tab="Загрузка видео" key="videos">
          <Card title="Загрузка видео">
            <Upload {...uploadProps}>
              <Button icon={<UploadOutlined />}>Нажмите для загрузки</Button>
            </Upload>
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title={selectedCourse ? 'Редактировать курс' : 'Создать новый курс'}
        visible={isCourseModalVisible}
        onCancel={() => {
          setIsCourseModalVisible(false);
          setSelectedCourse(null);
          courseForm.resetFields();
        }}
        footer={null}
      >
        <Form
          form={courseForm}
          layout="vertical"
          onFinish={selectedCourse ? handleUpdateCourse : handleCreateCourse}
        >
          <Form.Item
            name="title"
            label="Название курса"
            rules={[{ required: true, message: 'Введите название курса' }]}
          >
            <Input placeholder="Название курса" />
          </Form.Item>
          <Form.Item
            name="description"
            label="Описание курса"
            rules={[{ required: true, message: 'Введите описание курса' }]}
          >
            <Input.TextArea rows={4} placeholder="Описание курса" />
          </Form.Item>
          <Form.Item
            name="price"
            label="Цена курса"
            rules={[{ required: true, message: 'Введите цену курса' }]}
          >
            <InputNumber min={0} style={{ width: '100%' }} placeholder="Цена курса" />
          </Form.Item>
          <Form.Item
            name="is_active"
            label="Активность курса"
            valuePropName="checked"
            initialValue={true}
          >
            <Input type="checkbox" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              {selectedCourse ? 'Обновить курс' : 'Создать курс'}
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={selectedUser ? 'Редактировать пользователя' : 'Создать нового пользователя'}
        visible={isUserModalVisible}
        onCancel={() => {
          setIsUserModalVisible(false);
          setSelectedUser(null);
          userForm.resetFields();
        }}
        footer={null}
      >
        <Form
          form={userForm}
          layout="vertical"
          onFinish={selectedUser ? handleUpdateUser : handleCreateUser}
        >
          <Form.Item
            name="username"
            label="Имя пользователя"
            rules={[{ required: true, message: 'Введите имя пользователя' }]}
          >
            <Input placeholder="Имя пользователя" />
          </Form.Item>
          <Form.Item
            name="email"
            label="Email"
            rules={[{ required: true, message: 'Введите email' }]}
          >
            <Input placeholder="Email" />
          </Form.Item>
          {!selectedUser && (
            <Form.Item
              name="password"
              label="Пароль"
              rules={[{ required: true, message: 'Введите пароль' }]}
            >
              <Input.Password placeholder="Пароль" />
            </Form.Item>
          )}
          <Form.Item
            name="role"
            label="Роль"
            rules={[{ required: true, message: 'Выберите роль' }]}
          >
            <Input placeholder="student или admin" />
          </Form.Item>
          <Form.Item
            name="is_active"
            label="Активность пользователя"
            valuePropName="checked"
            initialValue={true}
          >
            <Input type="checkbox" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              {selectedUser ? 'Обновить пользователя' : 'Создать пользователя'}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default AdminPanel;
