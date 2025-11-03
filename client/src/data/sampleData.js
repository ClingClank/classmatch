// Sample data for development - will be replaced by Flask API + MySQL later

export const sampleCourses = [
  {
    id: "CS1101",
    code: "CS 1101",
    name: "Introduction to Computer Science",
    section: "001",
    instructor: "Dr. Sarah Johnson",
    schedule: "MWF 9:00-10:00 AM",
    students: 45,
    building: "Engineering Hall",
    room: "201",
  },
  {
    id: "CS2201",
    code: "CS 2201",
    name: "Data Structures and Algorithms",
    section: "002",
    instructor: "Prof. Michael Chen",
    schedule: "TR 2:00-3:30 PM",
    students: 38,
    building: "Science Building",
    room: "315",
  },
  {
    id: "CS3310",
    code: "CS 3310",
    name: "Database Systems",
    section: "001",
    instructor: "Dr. Emily Rodriguez",
    schedule: "MWF 11:00-12:00 PM",
    students: 32,
    building: "Engineering Hall",
    room: "405",
  },
  {
    id: "CS4090",
    code: "CS 4090",
    name: "Capstone Project I",
    section: "001",
    instructor: "Prof. David Williams",
    schedule: "MW 3:00-4:30 PM",
    students: 25,
    building: "Innovation Center",
    room: "102",
  },
  {
    id: "MATH2410",
    code: "MATH 2410",
    name: "Discrete Mathematics",
    section: "003",
    instructor: "Dr. Lisa Anderson",
    schedule: "TR 9:30-11:00 AM",
    students: 40,
    building: "Math Building",
    room: "210",
  },
  {
    id: "CS3320",
    code: "CS 3320",
    name: "Web Development",
    section: "001",
    instructor: "Prof. James Martinez",
    schedule: "TR 12:30-2:00 PM",
    students: 35,
    building: "Engineering Hall",
    room: "301",
  },
  {
    id: "CS2301",
    code: "CS 2301",
    name: "Computer Architecture",
    section: "002",
    instructor: "Dr. Robert Taylor",
    schedule: "MWF 1:00-2:00 PM",
    students: 42,
    building: "Science Building",
    room: "220",
  },
  {
    id: "CS3380",
    code: "CS 3380",
    name: "Artificial Intelligence",
    section: "001",
    instructor: "Dr. Amanda Lee",
    schedule: "TR 3:30-5:00 PM",
    students: 30,
    building: "Innovation Center",
    room: "205",
  },
];

export const sampleUsers = [
  {
    id: 1,
    email: "alice.smith@university.edu",
    password: "password123",
    name: "Alice Smith",
    major: "Computer Science",
    year: "Junior",
    avatar: "AS",
    bio: "Love coding and collaborative learning. Looking for serious study partners!",
    studyPreferences: {
      times: ["Morning", "Afternoon"],
      location: ["Library", "Coffee Shop"],
      style: "Group Discussion",
    },
    enrolledCourses: ["CS2201", "CS3310", "MATH2410"],
    availability: ["Monday 10am-12pm", "Wednesday 2pm-4pm", "Friday 1pm-3pm"],
  },
  {
    id: 2,
    email: "bob.johnson@university.edu",
    password: "password123",
    name: "Bob Johnson",
    major: "Computer Science",
    year: "Senior",
    avatar: "BJ",
    bio: "Senior CS major, happy to help underclassmen. Work-study friendly hours.",
    studyPreferences: {
      times: ["Evening", "Weekend"],
      location: ["Library", "Online"],
      style: "One-on-One",
    },
    enrolledCourses: ["CS4090", "CS3380"],
    availability: ["Tuesday 6pm-8pm", "Thursday 6pm-8pm", "Saturday 10am-2pm"],
  },
  {
    id: 3,
    email: "carol.williams@university.edu",
    password: "password123",
    name: "Carol Williams",
    major: "Software Engineering",
    year: "Sophomore",
    avatar: "CW",
    bio: "Passionate about web dev and databases. Let's build projects together!",
    studyPreferences: {
      times: ["Afternoon", "Evening"],
      location: ["Campus Center", "Online"],
      style: "Group Discussion",
    },
    enrolledCourses: ["CS2201", "CS3320", "CS3310"],
    availability: ["Monday 3pm-5pm", "Wednesday 3pm-5pm", "Friday 4pm-6pm"],
  },
  {
    id: 4,
    email: "david.brown@university.edu",
    password: "password123",
    name: "David Brown",
    major: "Computer Science",
    year: "Junior",
    avatar: "DB",
    bio: "Early bird coder. Prefer morning study sessions and structured learning.",
    studyPreferences: {
      times: ["Morning"],
      location: ["Library", "Engineering Lab"],
      style: "Structured Study",
    },
    enrolledCourses: ["CS2301", "MATH2410", "CS3310"],
    availability: ["Monday 8am-10am", "Wednesday 8am-10am", "Friday 9am-11am"],
  },
  {
    id: 5,
    email: "emma.davis@university.edu",
    password: "password123",
    name: "Emma Davis",
    major: "Data Science",
    year: "Junior",
    avatar: "ED",
    bio: "Data enthusiast! Looking for project partners and algorithm study buddies.",
    studyPreferences: {
      times: ["Afternoon", "Evening"],
      location: ["Library", "Coffee Shop"],
      style: "Project-Based",
    },
    enrolledCourses: ["CS2201", "CS3380", "MATH2410"],
    availability: ["Tuesday 2pm-5pm", "Thursday 2pm-5pm"],
  },
  {
    id: 6,
    email: "frank.miller@university.edu",
    password: "password123",
    name: "Frank Miller",
    major: "Computer Science",
    year: "Senior",
    avatar: "FM",
    bio: "Final year CS student. Capstone partner needed. Also tutoring data structures.",
    studyPreferences: {
      times: ["Afternoon", "Weekend"],
      location: ["Innovation Center", "Online"],
      style: "Project-Based",
    },
    enrolledCourses: ["CS4090", "CS3380"],
    availability: ["Monday 1pm-4pm", "Wednesday 1pm-4pm", "Saturday 2pm-6pm"],
  },
];

export const sampleGroups = [
  {
    id: "g1",
    name: "Data Structures Study Circle",
    courseId: "CS2201",
    courseName: "CS 2201 - Data Structures",
    owner: "alice.smith@university.edu",
    members: [
      "alice.smith@university.edu",
      "carol.williams@university.edu",
      "emma.davis@university.edu",
    ],
    description:
      "Weekly meetups to go over lecture material and practice coding problems together.",
    meetingTime: "Wednesdays 3:00 PM",
    location: "Library Study Room 3B",
    maxMembers: 6,
    tags: ["Algorithms", "Coding Practice", "Weekly Meetings"],
  },
  {
    id: "g2",
    name: "Capstone Project Team Alpha",
    courseId: "CS4090",
    courseName: "CS 4090 - Capstone",
    owner: "bob.johnson@university.edu",
    members: ["bob.johnson@university.edu", "frank.miller@university.edu"],
    description:
      "Building a student matching platform. Need frontend and backend developers.",
    meetingTime: "Mondays & Wednesdays 4:00 PM",
    location: "Innovation Center Room 102",
    maxMembers: 4,
    tags: ["Project Team", "Full Stack", "Agile"],
  },
  {
    id: "g3",
    name: "Database Design Workshop",
    courseId: "CS3310",
    courseName: "CS 3310 - Database Systems",
    owner: "alice.smith@university.edu",
    members: [
      "alice.smith@university.edu",
      "carol.williams@university.edu",
      "david.brown@university.edu",
    ],
    description:
      "Hands-on practice with SQL, normalization, and database design patterns.",
    meetingTime: "Fridays 2:00 PM",
    location: "Engineering Hall Lab 405",
    maxMembers: 5,
    tags: ["SQL", "Database Design", "Hands-on"],
  },
  {
    id: "g4",
    name: "AI & ML Study Group",
    courseId: "CS3380",
    courseName: "CS 3380 - Artificial Intelligence",
    owner: "emma.davis@university.edu",
    members: [
      "emma.davis@university.edu",
      "bob.johnson@university.edu",
      "frank.miller@university.edu",
    ],
    description:
      "Exploring machine learning algorithms and AI concepts. Python heavy!",
    meetingTime: "Thursdays 5:30 PM",
    location: "Online (Discord)",
    maxMembers: 8,
    tags: ["Machine Learning", "Python", "Theory + Practice"],
  },
];

// Helper function to get courses for a user
export function getUserCourses(userEmail) {
  const user = sampleUsers.find((u) => u.email === userEmail);
  if (!user) return [];

  return user.enrolledCourses
    .map((courseId) => sampleCourses.find((c) => c.id === courseId))
    .filter(Boolean);
}

// Helper function to find matching users based on shared courses
export function findMatches(userEmail) {
  const user = sampleUsers.find((u) => u.email === userEmail);
  if (!user) return [];

  return sampleUsers
    .filter((u) => u.email !== userEmail)
    .map((u) => {
      const sharedCourses = u.enrolledCourses.filter((courseId) =>
        user.enrolledCourses.includes(courseId)
      );
      return { ...u, sharedCourses, matchScore: sharedCourses.length };
    })
    .filter((u) => u.matchScore > 0)
    .sort((a, b) => b.matchScore - a.matchScore);
}

// Helper function to get groups for user's courses
export function getRelevantGroups(userEmail) {
  const user = sampleUsers.find((u) => u.email === userEmail);
  if (!user) return [];

  return sampleGroups.filter((group) =>
    user.enrolledCourses.includes(group.courseId)
  );
}
