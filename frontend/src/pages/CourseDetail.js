import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Typography, Button, List, Spin, message, Tag, Progress, Modal, Form, Input, InputNumber } from 'antd';
import { PlayCircleOutlined, BookOutlined, PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Paragraph, Text } = Typography;

const CourseDetail = ({ user }) => {
  const { id } = useParams();
  const [course, setCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isLessonModalVisible, setIsLessonModalVisible] = useState(false);
  const [lessonForm] = Form.useForm();

  useEffect(() => {
    fetchCourse();
    fetchLessons();
    if (user) {
      fetchProgress();
    }
  }, [id, user]);

  const fetchCourse = async () => {
    try {
      const response = await axios.get(`/courses/${id}`);
      setCourse(response.data);
    } catch (error) {
      message.error('Ошибка при загрузке курса');
      console.error('Ошибка при загрузке курса:', error);
    }
  };

  const fetchLessons = async () => {
    try {
      const response = await axios.get(`/courses/${id}/lessons`);
      setLessons(response.data);
    } catch (error) {
      message.error('Ошибка при загрузке уроков');
      console.error('Ошибка при загрузке уроков:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchProgress = async () => {
    try {
      const response = await axios.get(`/progress/${id}`);
      setProgress(response.data);
    } catch (error) {
      console.error('Ошибка при загрузке прогресса:', error);
    }
  };

  const handleCreateLesson = async (values) => {
    try {
      await axios.post('/lessons', { ...values, course_id: parseInt(id) });
      message.success('Урок успешно создан!');
      setIsLessonModalVisible(false);
      lessonForm.resetFields();
      fetchLessons();
    } catch (error) {
      message.error('Ошибка при создании урока');
      console.error('Ошибка при создании урока:', error);
    }
  };

  const handleUpdateProgress = async (lessonId) => {
    if (!user) {
      message.warning('Для отслеживания прогресса необходимо авторизоваться');
      return;
    }

    try {
      await axios.post(`/progress/${lessonId}`, { watched_seconds: 10, is_completed: true });
      message.success('Прогресс обновлен!');
      if (user) {
        fetchProgress();
      }
    } catch (error) {
      message.error('Ошибка при обновлении прогресса');
      console.error('Ошибка при обновлении прогресса:', error);
    }
  };

  const calculateProgress = () => {
    if (lessons.length === 0) return 0;
    const completedLessons = progress.filter(p => p.is_completed).length;
    return Math.round((completedLessons / lessons.length) * 100);
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!course) {
    return <div>Курс не найден</div>;
  }

  return (
    <div style={{ padding: '20px 0' }}>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <Title level={2}>{course.title}</Title>
            <Paragraph>{course.description}</Paragraph>
            <div style={{ marginTop: '10px' }}>
              <Tag color="green">{course.price} ₽</Tag>
              {course.is_active ? <Tag color="blue">Активен</Tag> : <Tag color="red">Неактивен</Tag>}
            </div>
          </div>
          {user && user.role === 'admin' && (
            <div>
              <Button icon={<EditOutlined />} style={{ marginRight: '10px' }}>
                Редактировать
              </Button>
              <Button icon={<DeleteOutlined />} danger>
                Удалить
              </Button>
            </div>
          )}
        </div>
      </Card>

      <Card style={{ marginTop: '20px' }}>
        <Title level={3}>Прогресс обучения</Title>
        {user ? (
          <Progress percent={calculateProgress()} status="active" />
        ) : (
          <Text type="secondary">Войдите, чтобы отслеживать прогресс</Text>
        )}
      </Card>

      <Card
        title="Уроки"
        extra={user && user.role === 'admin' && (
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setIsLessonModalVisible(true)}
          >
            Добавить урок
          </Button>
        )}
        style={{ marginTop: '20px' }}
      >
        <List
          itemLayout="horizontal"
          dataSource={lessons}
          renderItem={(lesson, index) => {
            const lessonProgress = progress.find(p => p.lesson_id === lesson.id);
            return (
              <List.Item
                actions={[
                  <Button
                    type="primary"
                    icon={<PlayCircleOutlined />}
                    onClick={() => handleUpdateProgress(lesson.id)}
                  >
                    Смотреть
                  </Button>
                ]}
              >
                <List.Item.Meta
                  avatar={<BookOutlined style={{ fontSize: '24px', color: '#1890ff' }} />}
                  title={`${index + 1}. ${lesson.title}`}
                  description={
                    <div>
                      <Paragraph ellipsis={{ rows: 2 }}>{lesson.description}</Paragraph>
                      {lessonProgress && (
                        <div style={{ marginTop: '10px' }}>
                          <Progress
                            percent={Math.round((lessonProgress.watched_seconds / (lesson.duration || 100)) * 100)}
                            size="small"
                          />
                        </div>
                      )}
                    </div>
                  }
                />
              </List.Item>
            );
          }}
        />
      </Card>

      <Modal
        title="Создать новый урок"
        visible={isLessonModalVisible}
        onCancel={() => setIsLessonModalVisible(false)}
        footer={null}
      >
        <Form
          form={lessonForm}
          layout="vertical"
          onFinish={handleCreateLesson}
        >
          <Form.Item
            name="title"
            label="Название урока"
            rules={[{ required: true, message: 'Введите название урока' }]}
          >
            <Input placeholder="Название урока" />
          </Form.Item>
          <Form.Item
            name="description"
            label="Описание урока"
          >
            <Input.TextArea rows={4} placeholder="Описание урока" />
          </Form.Item>
          <Form.Item
            name="duration"
            label="Длительность урока (в секундах)"
          >
            <InputNumber min={0} style={{ width: '100%' }} placeholder="Длительность урока" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Создать урок
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CourseDetail;
