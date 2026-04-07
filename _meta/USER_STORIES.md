# User Stories
## 三书精读出版系统 (Three Books Deep Reading & Publishing System)

**Document Version:** 1.0  
**Last Updated:** December 6, 2025  
**Format:** Agile User Stories

---

## Overview

User stories for the Three Books Deep Reading & Publishing System are organized by:
1. **User Role**: Project Lead, AI Assistant, Reader/Community
2. **Epic**: Daily Practice, Weekly Aggregation, Monthly Publishing, Book Building
3. **Priority**: Must Have (★★★), Should Have (★★), Nice to Have (★)

---

## EPIC 1: Daily Practice

### Story 1.1: As a Project Lead, I want to generate a daily note template

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want to generate a pre-formatted markdown template each morning so that I can quickly capture my reading insights without worrying about formatting.

**Acceptance Criteria:**
- [ ] Template includes date in YYYY-MM-DD format
- [ ] Template has sections: Summary, Key Insights, Modern Applications, Personal Reflection
- [ ] Template auto-includes word count (target 300-500 words)
- [ ] File is created in `daily-notes/drafts/` directory
- [ ] Template references current book being read

**Estimated Effort:** 2 points  
**Status:** Backlog

---

### Story 1.2: As a Project Lead, I want to track my daily reading progress

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want to see which sections/chapters I've completed for each book so that I can maintain consistent reading pace across the 7-year project.

**Acceptance Criteria:**
- [ ] Dashboard shows completion status per book
- [ ] Progress bar shows % complete for each text
- [ ] Can view historical reading dates
- [ ] Automatically updated from daily note filenames

**Estimated Effort:** 3 points  
**Status:** Backlog

---

### Story 1.3: As a Project Lead, I want to write daily notes in markdown format

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want to compose my insights using markdown so that I can maintain consistent formatting and leverage markdown tools throughout the publishing pipeline.

**Acceptance Criteria:**
- [ ] Markdown syntax is fully supported
- [ ] Notes support bold, italic, lists, quotes, code blocks
- [ ] Cross-reference capability between notes
- [ ] Live preview available

**Estimated Effort:** 1 point  
**Status:** Backlog

---

### Story 1.4: As a Project Lead, I want to publish daily notes to GitHub

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want to push my daily notes to GitHub so that I have version control, backup, and can track my progress over time.

**Acceptance Criteria:**
- [ ] Simple git commit command provided
- [ ] Automatic commit message generation
- [ ] Notes move from `drafts/` to `published/` folder
- [ ] Clear feedback on successful push
- [ ] Option to schedule publishing

**Estimated Effort:** 2 points  
**Status:** Backlog

---

### Story 1.5: As an AI Assistant, I want to suggest improvements to daily notes

**Priority:** ★★ (Should Have)  
**Narrative:**
> As an AI Assistant, I want to provide optional editing suggestions (grammar, clarity, flow) so that the Project Lead can improve note quality without manual editing overhead.

**Acceptance Criteria:**
- [ ] Suggestions are optional, non-intrusive
- [ ] Suggestions include: grammar, clarity, flow, relevance
- [ ] Project Lead can accept/reject suggestions
- [ ] Preserve original voice and perspective

**Estimated Effort:** 3 points  
**Status:** Backlog

---

## EPIC 2: Weekly Aggregation

### Story 2.1: As a Project Lead, I want automatic weekly summary generation

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want the system to automatically generate a weekly summary from my 7 daily notes so that I can save time and have coherent weekly themes emerge.

**Acceptance Criteria:**
- [ ] Automatically triggered every Saturday 08:00
- [ ] Summary reads 5-7 daily notes from past week
- [ ] Output is 1,000-2,000 words
- [ ] Summary created in `weekly-summaries/drafts/`
- [ ] Includes thematic clustering of daily insights
- [ ] Identifies cross-text patterns if applicable

**Estimated Effort:** 5 points  
**Status:** Backlog

---

### Story 2.2: As a Project Lead, I want to review and edit weekly summaries

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want to review AI-generated summaries and make manual edits before publishing so that the final output reflects my priorities and perspective.

**Acceptance Criteria:**
- [ ] Summary available for review by Friday evening
- [ ] Easy editing interface (markdown)
- [ ] Can add/remove sections
- [ ] Can reorder content
- [ ] Track changes feature available
- [ ] Publish to GitHub with one command

**Estimated Effort:** 2 points  
**Status:** Backlog

---

### Story 2.3: As a Reader, I want to subscribe to weekly summaries

**Priority:** ★★ (Should Have)  
**Narrative:**
> As a Reader, I want to receive notifications when new weekly summaries are published so that I can stay updated without checking the repository constantly.

**Acceptance Criteria:**
- [ ] Email subscription option available
- [ ] RSS feed available
- [ ] GitHub notifications work
- [ ] Unsubscribe option clear
- [ ] Frequency customizable

**Estimated Effort:** 4 points  
**Status:** Backlog

---

### Story 2.4: As an AI Assistant, I want to identify cross-text themes

**Priority:** ★ (Nice to Have)  
**Narrative:**
> As an AI Assistant, I want to identify patterns that appear across multiple classical texts so that the Project Lead can build connections for future synthesis work.

**Acceptance Criteria:**
- [ ] Identifies common themes across Art of War, Zizhi Tongjian, Bible
- [ ] Flags connections with confidence score
- [ ] Suggests potential integrated analysis
- [ ] Links to relevant daily notes

**Estimated Effort:** 5 points  
**Status:** Backlog

---

## EPIC 3: Monthly Publishing

### Story 3.1: As a Project Lead, I want automatic monthly report generation

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want the system to generate a monthly chapter synthesizing 4 weekly summaries into a comprehensive 5,000-word report so that monthly themes are captured at scale.

**Acceptance Criteria:**
- [ ] Automatically triggered first day of each month at 08:00
- [ ] Reads 4 previous weekly summaries
- [ ] Output is 4,000-6,000 words
- [ ] Created in appropriate book folder under `monthly-reports/`
- [ ] Includes introduction, section breakdown, conclusions
- [ ] Professional structure suitable for eventual publication

**Estimated Effort:** 5 points  
**Status:** Backlog

---

### Story 3.2: As a Project Lead, I want to generate PDF previews of monthly chapters

**Priority:** ★★ (Should Have)  
**Narrative:**
> As a Project Lead, I want to see what my monthly chapter will look like in PDF format so that I can evaluate layout, readability, and visual flow.

**Acceptance Criteria:**
- [ ] Converts markdown to PDF automatically
- [ ] Includes proper formatting (headers, spacing, fonts)
- [ ] PDF preview available within 1 hour of generation
- [ ] Can be shared with beta readers
- [ ] Professional appearance maintained

**Estimated Effort:** 3 points  
**Status:** Backlog

---

### Story 3.3: As a Project Lead, I want to manage monthly publication schedule

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want to see what months still need chapters and easily move chapters from draft to published so that I can maintain editorial calendar.

**Acceptance Criteria:**
- [ ] Calendar view showing completion status per month
- [ ] Visual indicator of draft vs. published chapters
- [ ] One-click publish action
- [ ] Undo/archive capability
- [ ] Monthly inventory report

**Estimated Effort:** 3 points  
**Status:** Backlog

---

### Story 3.4: As a Reader, I want to read published monthly chapters

**Priority:** ★★ (Should Have)  
**Narrative:**
> As a Reader, I want to access published monthly chapters in a readable format so that I can follow the Project Lead's learning journey.

**Acceptance Criteria:**
- [ ] Monthly chapters displayed on website/repository
- [ ] Easy navigation between chapters
- [ ] Search capability across chapters
- [ ] Clean, readable formatting
- [ ] Mobile-friendly display

**Estimated Effort:** 4 points  
**Status:** Backlog

---

## EPIC 4: Book Building & Publishing

### Story 4.1: As a Project Lead, I want to compile a complete book manuscript

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want to automatically compile monthly chapters into a structured manuscript for each book so that I have a complete draft ready for professional editing.

**Acceptance Criteria:**
- [ ] Can generate book manuscript for each text
- [ ] Includes all monthly chapters in chronological order
- [ ] Generates table of contents
- [ ] Generates index of key concepts
- [ ] Cross-references are functional
- [ ] Metadata included (publication date, version)

**Estimated Effort:** 5 points  
**Status:** Backlog

---

### Story 4.2: As a Project Lead, I want to export manuscript in multiple formats

**Priority:** ★★ (Should Have)  
**Narrative:**
> As a Project Lead, I want to export my completed manuscript as PDF, EPUB, and print-ready formats so that I can prepare for publication on multiple platforms.

**Acceptance Criteria:**
- [ ] PDF export with professional styling
- [ ] EPUB export for e-readers
- [ ] Print-ready PDF with proper margins
- [ ] Mobi format for Kindle
- [ ] All exports preserve formatting and cross-references

**Estimated Effort:** 4 points  
**Status:** Backlog

---

### Story 4.3: As a Project Lead, I want to manage book metadata

**Priority:** ★★ (Should Have)  
**Narrative:**
> As a Project Lead, I want to define and update book metadata (title, author, description, cover) so that my books have professional presentation across platforms.

**Acceptance Criteria:**
- [ ] Can set title, subtitle, author name
- [ ] Can write book description (500 words)
- [ ] Can specify publication date
- [ ] Can set ISBN/identifiers
- [ ] Can add cover image
- [ ] Metadata automatically included in exports

**Estimated Effort:** 2 points  
**Status:** Backlog

---

### Story 4.4: As a Project Lead, I want to track book progress by year

**Priority:** ★ (Nice to Have)  
**Narrative:**
> As a Project Lead, I want a comprehensive view of each book's progress toward completion so that I can adjust pace and maintain motivation across the 7-year timeline.

**Acceptance Criteria:**
- [ ] Shows estimated completion date per book
- [ ] Displays chapters completed vs. expected
- [ ] Projects final book length
- [ ] Identifies any behind-schedule work
- [ ] Suggests adjustment strategies

**Estimated Effort:** 3 points  
**Status:** Backlog

---

## EPIC 5: Community & Engagement

### Story 5.1: As a Reader, I want to discover notes by theme or book

**Priority:** ★★ (Should Have)  
**Narrative:**
> As a Reader, I want to search and filter notes by theme, book, or date so that I can explore topics of interest without reading linearly.

**Acceptance Criteria:**
- [ ] Search box for keyword queries
- [ ] Filter by book (Art of War, Zizhi Tongjian, Bible)
- [ ] Filter by date range
- [ ] Tag-based navigation
- [ ] "Related notes" suggestions

**Estimated Effort:** 3 points  
**Status:** Backlog

---

### Story 5.2: As a Reader, I want to provide feedback on published content

**Priority:** ★ (Nice to Have)  
**Narrative:**
> As a Reader, I want to leave comments and feedback on notes so that the Project Lead can gather insights and build community engagement.

**Acceptance Criteria:**
- [ ] Comment section per note/chapter
- [ ] GitHub discussions integration
- [ ] Email notification of comments
- [ ] Moderation tools for inappropriate content
- [ ] Reply capability for conversations

**Estimated Effort:** 4 points  
**Status:** Backlog

---

### Story 5.3: As a Community Member, I want to contribute annotations

**Priority:** ★ (Nice to Have)  
**Narrative:**
> As a Community Member, I want to submit optional annotations to notes so that the final published books include diverse perspectives.

**Acceptance Criteria:**
- [ ] Submission form for annotations
- [ ] Review/approval workflow
- [ ] Attribution to contributor
- [ ] Easy way to accept/integrate suggestions
- [ ] Recognition system for contributors

**Estimated Effort:** 5 points  
**Status:** Backlog

---

## EPIC 6: Automation & Infrastructure

### Story 6.1: As an AI System, I want to trigger workflows on schedule

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As an AI System, I want to automatically run generation tasks (daily templates, weekly summaries, monthly reports) on schedule so that the Project Lead doesn't need manual triggering.

**Acceptance Criteria:**
- [ ] Daily template generation at 06:00 each morning
- [ ] Weekly summary generation Saturday 08:00
- [ ] Monthly report generation 1st of month at 08:00
- [ ] Reliable execution with retry logic
- [ ] Failed jobs logged and reported

**Estimated Effort:** 4 points  
**Status:** Backlog

---

### Story 6.2: As a Project Lead, I want backup and disaster recovery

**Priority:** ★★★ (Must Have)  
**Narrative:**
> As a Project Lead, I want automatic backups of all content so that I'm protected against data loss across my 7-year project.

**Acceptance Criteria:**
- [ ] Daily backups to secondary location
- [ ] GitHub serves as primary backup
- [ ] Can restore from any point in time
- [ ] Verification that backups work
- [ ] Documentation of recovery procedure

**Estimated Effort:** 2 points  
**Status:** Backlog

---

### Story 6.3: As a Project Lead, I want comprehensive analytics

**Priority:** ★ (Nice to Have)  
**Narrative:**
> As a Project Lead, I want to see analytics about my writing (word counts, themes, consistency) so that I can track improvement and identify patterns.

**Acceptance Criteria:**
- [ ] Total words written per period (daily/weekly/monthly/yearly)
- [ ] Average note length trends
- [ ] Most common themes identified
- [ ] Consistency metrics (% days with notes)
- [ ] Visualization of progress over time

**Estimated Effort:** 4 points  
**Status:** Backlog

---

## User Story Template Reference

For creating additional user stories, use this format:

### Story [Epic].[Number]: As a [Role], I want to [Action]

**Priority:** ★★★/★★/★ ([Category])  
**Narrative:**
> As a [Role], I want to [Action] so that [Benefit].

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Estimated Effort:** N points  
**Status:** [Backlog/In Progress/Done]

---

## Release Planning

### MVP (Minimum Viable Product) - Q4 2025
- Story 1.1, 1.3, 1.4 (Daily workflow)
- Story 2.1, 2.2 (Weekly automation)
- Story 3.1, 3.3 (Monthly compilation)
- Story 6.1, 6.2 (Infrastructure)

### Release 1.0 - Q1 2026
- Add 1.2, 1.5 (Progress tracking, AI suggestions)
- Add 2.3 (Reader subscriptions)
- Add 3.2, 3.4 (PDF previews, reader access)
- Add 6.3 (Analytics)

### Release 2.0 - H1 2026
- Add 4.1, 4.2, 4.3 (Book compilation and export)
- Add 5.1, 5.2 (Community discovery and feedback)
- Add 4.4 (Progress tracking by year)

### Release 3.0+ - 2026+
- Add 5.3 (Community contributions)
- Add 2.4 (Cross-text themes)
- Ongoing refinement based on feedback

---

## Appendix: Related Documents

- `BRD.md` - Business Requirements Document
- `README.md` - Technical architecture
- `QUICK_START.md` - Quick reference
