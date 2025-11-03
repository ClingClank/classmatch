import React from "react";
import { Card, Badge, ListGroup } from "react-bootstrap";
import {
  FaUserGraduate,
  FaClock,
  FaMapMarkerAlt,
  FaBook,
} from "react-icons/fa";
import "./CourseCard.css";

const CourseCard = ({ course, onEnroll, isEnrolled = false }) => {
  return (
    <Card className="course-card shadow-sm h-100">
      <Card.Body>
        <div className="d-flex justify-content-between align-items-start mb-3">
          <div>
            <Badge bg="info" className="mb-2">
              {course.code}
            </Badge>
            <Card.Title className="h5 mb-1">{course.name}</Card.Title>
            <Card.Subtitle className="text-muted small">
              Section {course.section}
            </Card.Subtitle>
          </div>
          {isEnrolled && (
            <Badge bg="success" pill>
              Enrolled
            </Badge>
          )}
        </div>

        <ListGroup variant="flush" className="course-details mb-3">
          <ListGroup.Item className="course-detail-item">
            <FaUserGraduate className="me-2 text-primary" />
            <span className="small">{course.instructor}</span>
          </ListGroup.Item>
          <ListGroup.Item className="course-detail-item">
            <FaClock className="me-2 text-primary" />
            <span className="small">{course.schedule}</span>
          </ListGroup.Item>
          <ListGroup.Item className="course-detail-item">
            <FaMapMarkerAlt className="me-2 text-primary" />
            <span className="small">
              {course.building} - Room {course.room}
            </span>
          </ListGroup.Item>
          <ListGroup.Item className="course-detail-item">
            <FaBook className="me-2 text-primary" />
            <span className="small">{course.students} students enrolled</span>
          </ListGroup.Item>
        </ListGroup>

        {onEnroll && !isEnrolled && (
          <button
            className="btn btn-outline-primary w-100"
            onClick={() => onEnroll(course)}
          >
            Add to My Courses
          </button>
        )}
      </Card.Body>
    </Card>
  );
};

export default CourseCard;
