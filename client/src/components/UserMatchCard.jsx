import React from "react";
import { Card, Badge, Button, Row, Col } from "react-bootstrap";
import {
  FaGraduationCap,
  FaBookOpen,
  FaClock,
  FaEnvelope,
} from "react-icons/fa";
import "./UserMatchCard.css";

const UserMatchCard = ({ user, onMessage }) => {
  const sharedCourses = user.sharedCourses || [];

  return (
    <Card className="user-match-card shadow-sm mb-3">
      <Card.Body>
        <Row className="align-items-center">
          <Col xs="auto">
            <div className="user-avatar">{user.avatar}</div>
          </Col>
          <Col>
            <div className="d-flex justify-content-between align-items-start">
              <div>
                <h5 className="mb-1 text-white">{user.name}</h5>
                <div className="text-muted small mb-2">
                  <FaGraduationCap className="me-1" />
                  {user.major} • {user.year}
                </div>
              </div>
              <Badge bg="primary" pill>
                {user.matchScore} {user.matchScore === 1 ? "course" : "courses"}{" "}
                shared
              </Badge>
            </div>

            {user.bio && (
              <p className="small text-light-emphasis mb-2 mt-2">{user.bio}</p>
            )}

            {sharedCourses.length > 0 && (
              <div className="mb-2">
                <FaBookOpen className="me-2 text-primary" size={14} />
                <span className="small text-muted">Shared courses: </span>
                {sharedCourses.map((courseId, idx) => (
                  <Badge key={idx} bg="secondary" className="me-1" pill>
                    {courseId}
                  </Badge>
                ))}
              </div>
            )}

            {user.studyPreferences && (
              <div className="mb-2">
                <FaClock className="me-2 text-primary" size={14} />
                <span className="small text-muted">Prefers: </span>
                <span className="small text-light">
                  {user.studyPreferences.times?.join(", ")} •{" "}
                  {user.studyPreferences.style}
                </span>
              </div>
            )}

            {onMessage && (
              <Button
                variant="outline-primary"
                size="sm"
                className="mt-2"
                onClick={() => onMessage(user)}
              >
                <FaEnvelope className="me-2" />
                Send Message
              </Button>
            )}
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};

export default UserMatchCard;
