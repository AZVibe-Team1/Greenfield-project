# Dashboard Testing Guide

## 🚀 Quick Start Testing

### Step 1: Start the Application

```bash
# Make sure you're in the project root
cd /Users/FS/Documents/ASU_VibeCoding/Greenfield-project

# Start with the helper script (handles port conflicts)
./start.sh

# OR manually:
docker-compose up --build
```

Wait for these messages:
```
jobportal-backend   | ✅ Application startup complete
jobportal-frontend  | ▲ Next.js 14.1.0
jobportal-frontend  | - Local:        http://localhost:3000
```

### Step 2: Access the Application

Open your browser and go to: **http://localhost:3000**

---

## 🧪 Testing Scenarios

### Scenario 1: Test Job Seeker Dashboard (Emerald Theme)

#### 1.1 Register a New Job Seeker

1. Click **"Register"** on the landing page
2. Select **"Job Seeker"** role
3. Click **"Continue"**
4. Fill in the form:
   ```
   First Name: Alice
   Last Name: Johnson
   Email: alice.test@example.com
   Password: test123
   Confirm Password: test123
   Address: 789 Tech Street, Seattle, WA, 98101
   Phone: +12065551234
   Education Level: MS
   Field of Study: Computer Science
   Skills: Python, React, TypeScript, Node.js
   Salary Range: 80000 - 120000 (Yearly)
   ```
5. Click **"Create Account"**
6. You'll be redirected to login

#### 1.2 Login as Job Seeker

1. Email: `alice.test@example.com`
2. Password: `test123`
3. Role: **Job Seeker**
4. Click **"Login"**

#### 1.3 Verify Dashboard Elements

**✅ Check these items on the Seeker Dashboard:**

- [ ] **Header**
  - JobPortal logo with briefcase icon (emerald)
  - Your name displayed (Alice Johnson)
  - Logout button with icon

- [ ] **Welcome Banner**
  - Emerald gradient background
  - "Welcome back, Alice!" message
  - User icon visible

- [ ] **Statistics Cards (3 cards in a row)**
  - Total Applications card (emerald icon badge)
  - Profile Views card (blue icon badge) - shows random number
  - Saved Jobs card (amber icon badge) - shows 0

- [ ] **Quick Action Cards (3 cards)**
  - Search Jobs card with Search icon
  - My Applications card with FileText icon
  - My Profile card with User icon
  - Hover effects work (cards lift up)
  - Icons change color on hover

- [ ] **Profile Summary Section**
  - Section title with User icon
  - Education displayed with GraduationCap icon
  - Location displayed with MapPin icon
  - Desired Salary with DollarSign icon
  - Skills count with Star icon
  - Skills displayed as emerald tags (Python, React, TypeScript, Node.js)

- [ ] **Applications Section**
  - Shows "No Applications Yet" empty state (since you just registered)
  - Large FileText icon in gray circle
  - "Start applying to jobs" message
  - Green "Search Jobs" button

#### 1.4 Test Navigation

- [ ] Click **"Search Jobs"** button → should go to `/seeker/jobs`
- [ ] Click browser back button
- [ ] Click **"My Applications"** quick action → should go to `/seeker/applications`
- [ ] Click browser back button
- [ ] Click **"My Profile"** quick action → should go to `/seeker/profile`
- [ ] Click browser back button
- [ ] Click **JobPortal logo** in header → should go to home (then back to dashboard)

#### 1.5 Test Responsiveness

- [ ] Resize browser window to mobile size (< 640px)
- [ ] Statistics cards should stack vertically
- [ ] Action cards should stack vertically
- [ ] Your name in header should disappear on small screens
- [ ] Everything should remain readable

---

### Scenario 2: Test Employer Dashboard (Blue Theme)

#### 2.1 Logout and Register as Employer

1. Click **"Logout"** button
2. You'll be redirected to landing page
3. Click **"Register"**
4. Select **"Employer"** role
5. Click **"Continue"**
6. Fill in the form:
   ```
   Company Name: TechVentures Inc
   First Name: Bob
   Last Name: Smith
   Email: bob.test@techventures.com
   Password: test123
   Confirm Password: test123
   Address: 456 Business Blvd, Austin, TX, 78701
   Phone: +15125551234
   Benefits: Health insurance, 401k, Remote work, Stock options
   ```
7. Click **"Create Account"**

#### 2.2 Login as Employer

1. Email: `bob.test@techventures.com`
2. Password: `test123`
3. Role: **Employer**
4. Click **"Login"**

#### 2.3 Verify Dashboard Elements

**✅ Check these items on the Employer Dashboard:**

- [ ] **Header**
  - JobPortal logo with briefcase icon (blue)
  - Company name displayed (TechVentures Inc)
  - Logout button with icon

- [ ] **Welcome Banner**
  - Blue gradient background
  - "TechVentures Inc" company name
  - Building2 icon visible

- [ ] **Statistics Cards (4 cards in a row)**
  - Active Jobs card (blue icon badge) - shows 0
  - Applications card (green icon badge) - shows 0
  - Applicants card (purple icon badge) - shows 0
  - Match Rate card (amber icon badge) - shows 0%

- [ ] **Quick Action Cards (3 cards)**
  - Post a Job card with Plus icon
  - My Jobs card with Briefcase icon
  - Applications card with FileText icon
  - Hover effects work (cards lift up)
  - Icons change color on hover (white on blue)

- [ ] **Company Information Section**
  - Section title with Building2 icon
  - Company Name with Building2 icon
  - Location with MapPin icon
  - Primary Contact with Users icon
  - Active Postings with TrendingUp icon

- [ ] **Job Postings Section**
  - Shows "No Job Postings Yet" empty state
  - Large Briefcase icon in gray circle
  - "Create your first job posting" message
  - Blue "Post a Job" button with Plus icon

#### 2.4 Test Creating a Job Posting

- [ ] Click **"Post a Job"** button → should go to `/employer/jobs/new`
- [ ] Fill in the job posting form:
   ```
   Job Title: Senior Full Stack Developer
   Description: We're looking for an experienced developer...
   Department: Engineering
   Hiring Manager: Bob Smith
   Employment Type: Full-time
   Salary: 100000 - 150000 (Yearly)
   Education: BS
   Field: Computer Science
   Skills: Python, React, TypeScript, Docker
   ```
- [ ] Click **"Post Job"**
- [ ] You should be redirected back (possibly to jobs page)

#### 2.5 Verify Job Posted (Return to Dashboard)

- [ ] Navigate back to `/employer/dashboard` (via JobPortal logo or browser)
- [ ] **Statistics should update:**
  - Active Jobs should now show **1**
  - Other stats remain 0
- [ ] **Recent Job Postings section should show:**
  - Your job: "Senior Full Stack Developer"
  - Engineering department
  - Posted date (today)
  - Green "Posted" status badge with CheckCircle icon
  - "View →" link

#### 2.6 Test Navigation

- [ ] Click **"My Jobs"** quick action → should go to `/employer/jobs`
- [ ] Click browser back button
- [ ] Click **"Applications"** quick action → should go to `/employer/applications`
- [ ] Click browser back button
- [ ] Click **"View →"** on the job posting → should go to job detail page
- [ ] Click browser back button

---

### Scenario 3: Test Interaction Between Seeker and Employer

#### 3.1 Apply for Job as Seeker

1. **Logout** from employer account
2. **Login** as the seeker (alice.test@example.com / test123)
3. Click **"Search Jobs"** on dashboard
4. Find the "Senior Full Stack Developer" job
5. Click **"Apply Now"**
6. Confirm the application
7. Return to **Seeker Dashboard**

#### 3.2 Verify Seeker Dashboard Updates

**✅ Check these on Seeker Dashboard:**

- [ ] **Statistics updated:**
  - Total Applications should now show **1**
  - Profile Views still shows random number
  - Saved Jobs still shows 0

- [ ] **Recent Applications section changed:**
  - No longer shows empty state
  - Shows application card for the job
  - Displays job ID
  - Shows "Applied: [today's date]" with Clock icon
  - Status badge shows "Submitted" in blue with Clock icon

#### 3.3 Verify Employer Dashboard Updates

1. **Logout** from seeker account
2. **Login** as employer (bob.test@techventures.com / test123)
3. Go to **Employer Dashboard**

**✅ Check these on Employer Dashboard:**

- [ ] **Statistics updated:**
  - Active Jobs: 1
  - Applications: **1** (increased)
  - Applicants: **1** (increased)
  - Match Rate: shows calculated percentage

- [ ] **Recent Job Postings:**
  - Still shows the job
  - Status remains "Posted"

- [ ] Click **"Applications"** quick action
  - Should see Alice Johnson's application
  - Can view application details

---

## 🎨 Visual Testing Checklist

### Colors & Themes

**Seeker Dashboard (Emerald):**
- [ ] Banner is emerald gradient
- [ ] Primary buttons/icons are emerald-600
- [ ] Hover states are emerald-700
- [ ] Statistics card icons use emerald
- [ ] Skills tags are emerald-50 background with emerald-700 text

**Employer Dashboard (Blue):**
- [ ] Banner is blue gradient
- [ ] Primary buttons/icons are blue-600
- [ ] Hover states are blue-700
- [ ] Statistics card icons use blue
- [ ] Action cards hover to blue

### Icons

- [ ] All lucide-react icons display correctly
- [ ] Icons are properly sized and aligned
- [ ] Icon colors match the theme
- [ ] Icons in badges are centered

### Animations & Interactions

- [ ] Loading spinner appears when dashboard first loads
- [ ] Cards have subtle shadow
- [ ] Action cards lift on hover (-translate-y-1)
- [ ] Icons change color on hover
- [ ] Transitions are smooth (not jumpy)
- [ ] Buttons show hover states

### Responsive Design

Test at these breakpoints:
- [ ] **Mobile (375px):** Cards stack, text readable
- [ ] **Tablet (768px):** Cards in grid, some stacking
- [ ] **Desktop (1280px):** Full layout, all cards in rows

---

## 🐛 Common Issues & Solutions

### Issue: Port 3000 already in use
```bash
# Solution: Use start script
./start.sh

# OR manually kill process
lsof -ti:3000 | xargs kill -9
docker-compose up --build
```

### Issue: Cannot connect to backend
```bash
# Check backend is running
curl http://localhost:8000/health

# Check docker logs
docker-compose logs backend
```

### Issue: Dashboard shows "Loading..." forever
- Check browser console for errors (F12)
- Verify JWT token in localStorage
- Try logging out and back in
- Check backend API is responding

### Issue: Icons not showing
- Check that lucide-react is installed
- Rebuild frontend: `docker-compose build --no-cache frontend`
- Check browser console for import errors

### Issue: Styles look wrong
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check Tailwind CSS is working
- Inspect element to verify classes are applied

---

## ✅ Final Checklist

- [ ] Both dashboards load without errors
- [ ] Loading states display correctly
- [ ] Empty states display correctly
- [ ] Data displays correctly when present
- [ ] All navigation links work
- [ ] Logout works from both dashboards
- [ ] Role-based routing works (seeker can't access employer routes)
- [ ] Responsive design works on mobile
- [ ] All hover effects work
- [ ] Colors match the design system
- [ ] Icons display correctly
- [ ] No console errors in browser
- [ ] No TypeScript errors in terminal

---

## 📸 Screenshots to Take (Optional)

If documenting for team:
1. Seeker dashboard with no applications (empty state)
2. Seeker dashboard with applications
3. Employer dashboard with no jobs (empty state)
4. Employer dashboard with jobs posted
5. Mobile view of both dashboards
6. Hover states on action cards

---

## 🎉 Success Criteria

**Testing is successful if:**
1. ✅ Both dashboards load and display correctly
2. ✅ All role-based theming works (emerald vs blue)
3. ✅ Statistics update based on user actions
4. ✅ Empty states show when no data
5. ✅ Navigation works between all pages
6. ✅ Responsive design works on different screen sizes
7. ✅ No errors in browser console
8. ✅ Authentication and logout work properly

---

**Happy Testing! 🚀**

Need help with any issues? Check the troubleshooting section or review the documentation:
- `DASHBOARD_UPDATE.md` - Dashboard design documentation
- `frontend_md/QUICKSTART.md` - General quick start guide
- `frontend_md/TEST_CREDENTIALS.md` - Test account info

