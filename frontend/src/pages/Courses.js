import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Typography, Button, Spin, message, Tag, Modal, Form, Input, InputNumber } from 'antd';
import { BookOutlined, PlusOutlined, DollarOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Paragraph, Text } = Typography;

const Courses = ({ user }) => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get('/courses');
      setCourses(response.data);
    } catch (error) {
      message.error('Ошибка при загрузке курсов');
      console.error('Ошибка при загрузке курсов:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = async (courseId) => {
    if (!user) {
      message.warning('Для покупки курса необходимо авторизоваться');
      window.location.href = '/login';
      return;
    }

    try {
      await axios.post(`/courses/${courseId}/purchase`);
      message.success('Курс успешно приобретен!');
      fetchCourses();
    } catch (error) {
      message.error('Ошибка при покупке курса');
      console.error('Ошибка при покупке курса:', error);
    }
  };

  const handleCreateCourse = async (values) => {
    try {
      await axios.post('/courses', values);
      message.success('Курс успешно создан!');
      setIsModalVisible(false);
      form.resetFields();
      fetchCourses();
    } catch (error) {
      message.error('Ошибка при создании курса');
      console.error('Ошибка при создании курса:', error);
    }
  };

  return (
    <div style={{ padding: '20px 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <Title level={2}>Курсы</Title>
        {user && user.role === 'admin' && (
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setIsModalVisible(true)}
          >
            Создать курс
          </Button>
        )}
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <Spin size="large" />
        </div>
      ) : (
        <Row gutter={[16, 16]}>
          {courses.map(course => (
            <Col xs={24} sm={12} md={8} key={course.id}>
              <Card
                hoverable
                cover={<div style={{ height: '150px', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#f0f2f5' }}><BookOutlined style={{ fontSize: '60px', color: '#1890ff' }} /></div>}
                actions={[
                  <Button type="primary" onClick={() => window.location.href = `/courses/${course.id}`}>
                    Подробнее
                  </Button>,
                  <Button icon={<DollarOutlined />} onClick={() => handlePurchase(course.id)}>
                    Купить
                  </Button>
                ]}
              >
                <Card.Meta
                  title={course.title}
                  description={
                    <div>
                      <Paragraph ellipsis={{ rows: 2 }}>{course.description}</Paragraph>
                      <div style={{ marginTop: '10px' }}>
                        <Tag color="green">{course.price} ₽</Tag>
                        {course.is_active ? <Tag color="blue">Активен</Tag> : <Tag color="red">Неактивен</Tag>}
                      </div>
                    </div>
                  }
                />
              </Card>
            </Col>
          ))}
        </Row>
      )}

      <Modal
        title="Создать новый курс"
        visible={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreateCourse}
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
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Создать курс
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Courses;
