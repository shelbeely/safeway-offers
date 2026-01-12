# Safeway API Status Report

**Last Updated:** January 2026

## Executive Summary

Based on research conducted in January 2026, the Safeway mobile API endpoints used by this tool **appear to still be operational**, though they remain unofficial and undocumented.

## API Endpoints Used

This tool interacts with the following Safeway API endpoints:

1. **OAuth Authentication**: `https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/token`
   - Used for user authentication via OAuth 2.0
   - Managed by Okta (Albertsons/Safeway's identity provider)

2. **Manufacturer Coupons**: `https://nimbus.safeway.com/emmd/service/gallery/offer/mfg`
   - Retrieves available manufacturer coupons

3. **Personalized Offers**: `https://nimbus.safeway.com/emmd/service/gallery/offer/pd`
   - Retrieves personalized offers based on shopping history

4. **Add Offers**: `https://nimbus.safeway.com/Clipping1/services/clip/items`
   - Clips/loads offers to user account

5. **Shopping List**: `https://nimbus.safeway.com/emmd/service/mylist/default/details`
   - Retrieves currently loaded offers

## Research Findings (January 2026)

### API Availability
- The `nimbus.safeway.com` endpoint remains functional as the backend for Safeway's mobile app
- Active GitHub repositories and community scripts continue to use these endpoints as of 2025-2026
- Multiple third-party data scraping services report ongoing access to Safeway APIs

### Authentication System
- Safeway/Albertsons uses **Okta** as their core identity platform
- OAuth 2.0 with Multi-Factor Authentication (MFA) support
- The authentication system receives regular updates (2024-2026 timeline shows ongoing enhancements)
- Okta API receives bug fixes, feature additions, and security improvements regularly

### Important Caveats

⚠️ **This is an UNOFFICIAL API**
- Not documented or officially supported by Safeway/Albertsons
- No public developer program or API documentation
- Subject to change without notice
- Usage may violate terms of service

⚠️ **Stability Concerns**
- API endpoints can change at any time
- OAuth client IDs and secrets may be rotated
- Authentication flows may be updated
- New security measures could break existing implementations

## What This Means for Users

### Current Status (2026)
✅ **Likely Working**: Based on research, the API should still function
- Authentication endpoint is actively maintained by Okta
- Mobile app backend (`nimbus.safeway.com`) remains operational
- Community reports suggest continued functionality

### Future Outlook
⚠️ **Uncertain**: The API could stop working at any time
- Safeway may deprecate or change the API
- New security measures could break authentication
- Mobile app updates might use different endpoints

## If the Tool Stops Working

If you encounter issues, try these steps in order:

### 1. Verify API Status
Run the built-in API checker:
```bash
./pantrypilot -check-api
```

### 2. Test Official App
Log into the official Safeway mobile app with your credentials. If that works but this tool doesn't, the API has likely changed.

### 3. Check for Updates
- Look for updated versions of this tool
- Check GitHub issues and pull requests
- Search for community forks with updated endpoints

### 4. Investigate API Changes
If you have technical skills, you can investigate what changed:

**Tools Needed:**
- Charles Proxy, mitmproxy, or similar HTTPS inspection tool
- The official Safeway mobile app
- A test device or emulator

**Steps:**
1. Set up an HTTPS proxy to intercept mobile app traffic
2. Log into the Safeway app and navigate through the offers
3. Observe the API calls made by the app
4. Note any changes to:
   - API endpoints (URLs)
   - Authentication methods
   - Request/response formats
   - OAuth client credentials

**Reference:** For a detailed guide on reverse engineering private APIs, see:
https://blog.jonlu.ca/posts/safeway

## Technical Details

### Authentication Flow
1. Client sends username/password to Okta OAuth endpoint
2. Okta validates credentials and returns access token
3. Access token is used as Bearer token in subsequent API calls
4. Token is also sent as a cookie (`swyConsumerDirectoryPro`)

### Request Headers
```
Authorization: Bearer <access_token>
User-Agent: Safeway/3373 CFNetwork/978.0.7 Darwin/18.6.0
Content-Type: application/json
```

### Client Credentials (Current)
- **Client ID**: `0oap6kkp7Sefg24rB2p6`
- **Client Secret**: `4UpmzD4hlF2VYQqYjDUoamgLu2Bo1OzagpfG7yus`

⚠️ **Note**: These credentials are embedded in the mobile app and could change in future app updates.

## Data Sources

This report is based on:
- Web research conducted in January 2026
- Okta API documentation and release notes (2024-2026)
- Community tools and scripts using Safeway APIs
- Third-party data integration services
- Blog posts about Safeway API reverse engineering

## Recommendations

### For Users
- Use this tool while it works, but have a backup plan
- Consider manually loading offers if the tool stops working
- Don't rely solely on this tool for critical savings

### For Developers
- Monitor Okta's API release notes for authentication changes
- Keep an eye on community forums for reports of API issues
- Consider implementing fallback mechanisms
- Add better error handling and user feedback

## Contributing

If you discover that the API has changed:
1. Open a GitHub issue with details
2. If possible, provide updated endpoint information
3. Submit a pull request with fixes

## Legal and Ethical Considerations

- This tool uses unofficial APIs not intended for third-party access
- Using this tool may violate Safeway's terms of service
- Use at your own risk
- Respect rate limits and don't abuse the API
- Consider the ethical implications of automated coupon clipping

## References

- [Reversing private APIs, Safeway, and not-so-extreme couponing](https://blog.jonlu.ca/posts/safeway)
- [Okta Identity Engine API Release Notes](https://developer.okta.com/docs/release-notes/2024-okta-identity-engine/)
- [Albertsons + Okta Case Study](https://www.okta.com/customers/albertsons/)
- [Okta Authentication API Documentation](https://developer.okta.com/docs/reference/api/authn/)
