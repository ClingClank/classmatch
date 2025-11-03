import React, { useState, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Badge,
  Button,
  Tabs,
  Tab,
} from "react-bootstrap";
import { FaBook, FaUsers, FaUserFriends, FaPlus } from "react-icons/fa";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import {
  getUserCourses,
  getRelevantGroups,
  findMatches,
} from "../../data/sampleData";
import CourseCard from "../../components/CourseCard/CourseCard";
import GroupCard from "../../components/GroupCard/GroupCard";
import "./Dashboard.css";

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [relevantGroups, setRelevantGroups] = useState([]);
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    if (user) {
      setEnrolledCourses(getUserCourses(user.email));
      setRelevantGroups(getRelevantGroups(user.email));
      setMatches(findMatches(user.email).slice(0, 3));
    }
  }, [user]);

  if (!user) {
    return null; // Protected route will handle redirect
  }

  const stats = [
    {
      icon: FaBook,
      label: "Enrolled Courses",
      value: enrolledCourses.length,
      color: "primary",
    },
    {
      icon: FaUsers,
      label: "Study Groups",
      value: relevantGroups.length,
      color: "success",
    },
    {
      icon: FaUserFriends,
      label: "Potential Matches",
      value: matches.length,
      color: "info",
    },
  ];

  return (
    <Container className="dashboard-page py-4">
      {/* Welcome Header */}
      <div className="welcome-header mb-4">
        <Row className="align-items-center">
          <Col>
            <h1 className="display-6 fw-bold text-white mb-2">
              Welcome back, {user.name?.split(" ")[0] || "Student"}!
            </h1>
            <p className="text-muted lead mb-0">
              Here's what's happening with your classes today
            </p>
          </Col>
          <Col xs="auto" className="d-none d-md-block">
            <div className="user-avatar-large">{user.avatar}</div>
          </Col>
        </Row>
      </div>

      {/* Stats Cards */}
      <Row className="g-3 mb-4">
        {stats.map((stat, idx) => (
          <Col key={idx} xs={12} md={4}>
            <Card className="stat-card shadow-sm h-100">
              <Card.Body className="d-flex align-items-center">
                <div className={`stat-icon bg-${stat.color}`}>
                  <stat.icon size={24} />
                </div>
                <div className="ms-3">
                  <h3 className="mb-0 fw-bold text-white">{stat.value}</h3>
                  <p className="mb-0 text-muted small">{stat.label}</p>
                </div>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      {/* Main Content Tabs */}
      <Card className="main-content-card shadow-sm">
        <Card.Body className="p-0">
          <Tabs defaultActiveKey="courses" className="dashboard-tabs">
            {/* My Courses Tab */}
            <Tab
              eventKey="courses"
              title={
                <>
                  <FaBook className="me-2" />
                  My Courses
                </>
              }
            >
              <div className="p-4">
                {enrolledCourses.length === 0 ? (
                  <div className="empty-state text-center py-5">
                    <FaBook size={64} className="text-muted mb-3" />
                    <h4 className="text-light mb-3">No Courses Yet</h4>
                    <p className="text-muted mb-4">
                      Start by browsing available courses and adding them to
                      your schedule
                    </p>
                    <Button
                      variant="primary"
                      size="lg"
                      onClick={() => navigate("/browse-courses")}
                    >
                      <FaPlus className="me-2" />
                      Browse Courses
                    </Button>
                  </div>
                ) : (
                  <>
                    <div className="d-flex justify-content-between align-items-center mb-3">
                      <h5 className="text-light mb-0">
                        Enrolled Courses ({enrolledCourses.length})
                      </h5>
                      <Button
                        variant="primary"
                        size="sm"
                        onClick={() => navigate("/browse-courses")}
                      >
                        <FaPlus className="me-1" />
                        Add More
                      </Button>
                    </div>
                    <Row xs={1} md={2} lg={3} className="g-3">
                      {enrolledCourses.map((course) => (
                        <Col key={course.id}>
                          <CourseCard course={course} isEnrolled={true} />
                        </Col>
                      ))}
                    </Row>
                  </>
                )}
              </div>
            </Tab>

            {/* Study Groups Tab */}
            <Tab
              eventKey="groups"
              title={
                <>
                  <FaUsers className="me-2" />
                  Study Groups
                </>
              }
            >
              <div className="p-4">
                {relevantGroups.length === 0 ? (
                  <div className="empty-state text-center py-5">
                    <FaUsers size={64} className="text-muted mb-3" />
                    <h4 className="text-light mb-3">No Study Groups Found</h4>
                    <p className="text-muted mb-4">
                      Enroll in courses to see relevant study groups or create
                      your own
                    </p>
                    <Button
                      variant="primary"
                      size="lg"
                      onClick={() => navigate("/create-group")}
                    >
                      <FaPlus className="me-2" />
                      Create Study Group
                    </Button>
                  </div>
                ) : (
                  <>
                    <div className="d-flex justify-content-between align-items-center mb-3">
                      <h5 className="text-light mb-0">
                        Available Groups ({relevantGroups.length})
                      </h5>
                      <Button
                        variant="outline-primary"
                        size="sm"
                        onClick={() => navigate("/create-group")}
                      >
                        <FaPlus className="me-1" />
                        Create Group
                      </Button>
                    </div>
                    <Row xs={1} md={2} className="g-3">
                      {relevantGroups.map((group) => (
                        <Col key={group.id}>
                          <GroupCard group={group} />
                        </Col>
                      ))}
                    </Row>
                  </>
                )}
              </div>
            </Tab>

            {/* Matches Tab */}
            <Tab
              eventKey="matches"
              title={
                <>
                  <FaUserFriends className="me-2" />
                  Matches
                </>
              }
            >
              <div className="p-4">
                {matches.length === 0 ? (
                  <div className="empty-state text-center py-5">
                    <FaUserFriends size={64} className="text-muted mb-3" />
                    <h4 className="text-light mb-3">No Matches Yet</h4>
                    <p className="text-muted mb-4">
                      Add courses to find classmates with similar schedules
                    </p>
                    <Button
                      variant="primary"
                      size="lg"
                      onClick={() => navigate("/browse-courses")}
                    >
                      Browse Courses
                    </Button>
                  </div>
                ) : (
                  <>
                    <div className="d-flex justify-content-between align-items-center mb-3">
                      <h5 className="text-light mb-0">Top Matches</h5>
                      <Button
                        variant="outline-primary"
                        size="sm"
                        onClick={() => navigate("/matches")}
                      >
                        View All
                      </Button>
                    </div>
                    {matches.map((match, idx) => (
                      <Card key={idx} className="match-preview-card mb-3">
                        <Card.Body className="d-flex align-items-center">
                          <div className="match-avatar me-3">
                            {match.avatar}
                          </div>
                          <div className="flex-grow-1">
                            <h6 className="mb-1 text-white">{match.name}</h6>
                            <p className="mb-0 text-muted small">
                              {match.major} • {match.year}
                            </p>
                          </div>
                          <Badge bg="primary" pill>
                            {match.matchScore} shared
                          </Badge>
                        </Card.Body>
                      </Card>
                    ))}
                  </>
                )}
              </div>
            </Tab>
          </Tabs>
        </Card.Body>
      </Card>
    </Container>
  );
}
