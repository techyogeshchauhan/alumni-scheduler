# Navbar and Functionality Debug Guide

## Common Issues and Solutions

### 1. Dropdown Menus Not Working
**Symptoms**: Dropdowns don't open on hover or click
**Solutions**:
- Check JavaScript console for errors
- Ensure Tailwind CSS is loaded
- Verify dropdown JavaScript is running
- Check for conflicting CSS

### 2. CSRF Token Errors (400 Bad Request)
**Symptoms**: Forms return 400 errors
**Solutions**:
- Add `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>` to forms
- Ensure CSRF protection is enabled in Flask
- Check form method is POST

### 3. Graduation Year Sorting Error
**Symptoms**: TypeError when accessing directory
**Solutions**:
- Convert graduation years to integers before sorting
- Filter out None/invalid values
- Handle mixed data types

### 4. ObjectId Serialization Error
**Symptoms**: JSON serialization errors in calendar
**Solutions**:
- Convert ObjectIds to strings before JSON serialization
- Use str(object_id) for MongoDB ObjectIds

### 5. Mobile Menu Issues
**Symptoms**: Mobile menu doesn't toggle
**Solutions**:
- Check mobile menu JavaScript
- Verify button click handlers
- Test on actual mobile devices

## Testing Steps

1. **Start Application**:
   ```bash
   python app.py
   ```

2. **Test User Flows**:
   - Register new user
   - Login as alumni
   - Login as admin
   - Test all navbar links
   - Test dropdown menus
   - Test mobile responsiveness

3. **Check Browser Console**:
   - Open Developer Tools (F12)
   - Check Console tab for JavaScript errors
   - Check Network tab for failed requests

4. **Test Forms**:
   - RSVP to events
   - Post comments
   - Edit profile
   - Create events (admin)

## Browser Compatibility

- Chrome: ✅ Fully supported
- Firefox: ✅ Fully supported  
- Safari: ✅ Fully supported
- Edge: ✅ Fully supported
- Mobile browsers: ✅ Responsive design

## Performance Tips

- Use browser caching for static files
- Minimize JavaScript execution
- Optimize CSS delivery
- Use CDN for external libraries
