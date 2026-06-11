import React from 'react';
import { Card, Row, Col, Typography, Button, Space } from 'antd';
import { BookOutlined, PlayCircleOutlined, TrophyOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

const Dashboard = ({ user }) => {
  return (
    <div style={{ padding: '20px 0' }}>
      <Title level={2}>Добро пожаловать в AsyncLearn LMS!</Title>
      <Paragraph>
        Платформа онлайн-обучения с видеоуроками, платежами и системой отслеживания прогресса.
      </Paragraph>

      <Row gutter={[16, 16]} style={{ marginTop: '30px' }}>
        <Col xs={24} sm={12} md={8}>
          <Card
            hoverable
            cover={<div style={{ height: '150px', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#f0f2f5' }}><BookOutlined style={{ fontSize: '60px', color: '#1890ff' }} /></div>}
          >
            <Card.Meta
              title="Курсы"
              description="Доступ к широкому спектру курсов по различным темам"
            />
            <Button type="primary" block style={{ marginTop: '10px' }} onClick={() => window.location.href = '/courses'}>
              Смотреть курсы
            </Button>
          </Card>
        </Col>

        <Col xs={24} sm={12} md={8}>
          <Card
            hoverable
            cover={<div style={{ height: '150px', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#f0f2f5' }}><PlayCircleOutlined style={{ fontSize: '60px', color: '#52c41a' }} /></div>}
          >
            <Card.Meta
              title="Видеоуроки"
              description="Качественные видеоуроки от лучших преподавателей"
            />
            <Button type="primary" block style={{ marginTop: '10px' }} onClick={() => window.location.href = '/courses'}>
              Начать обучение
            </Button>
          </Card>
        </Col>

        <Col xs={24} sm={12} md={8}>
          <Card
            hoverable
            cover={<div style={{ height: '150px', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: '#f0f2f5' }}><TrophyOutlined style={{ fontSize: '60px', color: '#faad14' }} /></div>}
          >
            <Card.Meta
              title="Достижения"
              description="Отслеживайте свой прогресс и получайте достижения"
            />
            <Button type="primary" block style={{ marginTop: '10px' }} onClick={() => window.location.href = '/courses'}>
              Мой прогресс
            </Button>
          </Card>
        </Col>
      </Row>

      <Card style={{ marginTop: '30px' }}>
        <Title level={3}>О платформе</Title>
        <Paragraph>
          AsyncLearn LMS - это современная платформа онлайн-обучения, которая использует передовые технологии
          для обеспечения качественного образовательного процесса. Наша платформа позволяет:
        </Paragraph>
        <ul>
          <li>Изучать курсы в удобном для вас темпе</li>
          <li>Отслеживать свой прогресс в реальном времени</li>
          <li>Получать сертификаты после завершения курсов</li>
          <li>Взаимодействовать с преподавателями и другими студентами</li>
        </ul>
      </Card>
    </div>
  );
};

export default Dashboard;
