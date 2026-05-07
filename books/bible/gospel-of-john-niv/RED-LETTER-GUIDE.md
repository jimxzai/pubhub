# Red Letter Bible - Jesus's Words in Red

**Inspired by**: ai-eden.com
**Color**: #CC0000 (Classic Red Letter Bible red)
**Implementation**: LaTeX `\jesus{}` command

---

## 📖 Overview

Following the red letter Bible tradition (inspired by ai-eden.com), Jesus's direct speech is displayed in **red** in the Gospel of John PDF to make His words stand out visually.

**Color Definition**:
```latex
\definecolor{JesusRed}{RGB}{204,0,0}  % #CC0000
```

**Usage Command**:
```latex
\newcommand{\jesus}[1]{\textcolor{JesusRed}{#1}}
```

---

## ✍️ How to Mark Jesus's Words

### In Markdown Files

When writing Gospel of John chapters, wrap Jesus's direct speech with the LaTeX command `\jesus{}`:

#### Example 1: John 14:6

```markdown
### English — NIV (New International Version)

> ^6^Jesus said to him, \jesus{"I am the way, and the truth, and the life. No one comes to the Father except through me."}
```

#### Example 2: John 3:16-17

```markdown
### 中文 — 和合本修訂版 (RCUV)

> ^16^\jesus{「神愛世人，甚至將他獨一的兒子賜給他們，叫一切信他的人不致滅亡，反得永生。^17^因為神差他的兒子到世上來，不是要定世人的罪，而是要使世人因他得救。」}
```

#### Example 3: John 1:51

```markdown
> ^51^He said to him, \jesus{"Truly, truly, I say to you, you will see heaven opened, and the angels of God ascending and descending on the Son of Man."}
```

---

## 📋 Complete List - Jesus's Words in John

### Chapter 1: Introduction & First Disciples
- **1:38** - \jesus{"What are you seeking?"}
- **1:39** - \jesus{"Come and you will see."}
- **1:42** - \jesus{"You are Simon... You shall be called Cephas"}
- **1:43** - \jesus{"Follow me."}
- **1:48** - \jesus{"Before Philip called you... I saw you"}
- **1:50-51** - \jesus{"Because I said... you will see greater things"}

### Chapter 2: Cana Wedding & Temple Cleansing
- **2:4** - \jesus{"Woman, what does this have to do with me? My hour has not yet come."}
- **2:16** - \jesus{"Take these things away; do not make my Father's house a house of trade."}
- **2:19** - \jesus{"Destroy this temple, and in three days I will raise it up."}

### Chapter 3: Nicodemus - Born Again
- **3:3** - \jesus{"Truly, truly, I say to you, unless one is born again..."}
- **3:5-21** - Extended teaching on new birth (ENTIRE DISCOURSE in red)

### Chapter 4: Samaritan Woman - Living Water
- **4:7** - \jesus{"Give me a drink."}
- **4:10** - \jesus{"If you knew the gift of God..."}
- **4:13-14** - \jesus{"Everyone who drinks of this water... will never be thirsty"}
- **4:16-26** - Extended conversation (FULL DIALOGUE in red)
- **4:32** - \jesus{"I have food to eat that you do not know about."}
- **4:34-38** - Teaching on spiritual harvest

### Chapter 5: Bethesda Healing - Divine Authority
- **5:6** - \jesus{"Do you want to be healed?"}
- **5:8** - \jesus{"Get up, take up your bed, and walk."}
- **5:14** - \jesus{"See, you are well! Sin no more..."}
- **5:17-47** - Major discourse on Son's authority (ENTIRE TEACHING in red)

### Chapter 6: Bread of Life Discourse
- **6:5** - \jesus{"Where are we to buy bread..."}
- **6:10** - \jesus{"Have the people sit down."}
- **6:20** - \jesus{"It is I; do not be afraid."}
- **6:26-71** - BREAD OF LIFE DISCOURSE (ENTIRE CHAPTER mostly Jesus's words!)

### Chapter 7: Feast of Tabernacles
- **7:6-8** - \jesus{"My time has not yet come..."}
- **7:16-24** - Teaching about His doctrine
- **7:28-29** - \jesus{"You know me, and you know where I come from..."}
- **7:33-34** - \jesus{"I will be with you a little longer..."}
- **7:37-38** - \jesus{"If anyone thirsts, let him come to me and drink..."}

### Chapter 8: Light of the World - "I AM"
- **8:7** - \jesus{"Let him who is without sin... cast the first stone"}
- **8:10-11** - \jesus{"Woman, where are they?... Neither do I condemn you"}
- **8:12** - \jesus{"I am the light of the world..."}
- **8:14-59** - Extended "I AM" discourse (MOST OF CHAPTER in red)
  - **8:58** - \jesus{"Truly, truly, I say to you, before Abraham was, I AM."}

### Chapter 9: Man Born Blind
- **9:3-5** - \jesus{"It was not that this man sinned... I am the light of the world"}
- **9:35-38** - Revelation to the healed man
- **9:39-41** - Judgment pronouncement

### Chapter 10: Good Shepherd
- **10:1-30** - GOOD SHEPHERD DISCOURSE (ENTIRE PARABLE in red!)
  - **10:7** - \jesus{"I am the door of the sheep"}
  - **10:9** - \jesus{"I am the door. If anyone enters by me..."}
  - **10:11** - \jesus{"I am the good shepherd..."}
  - **10:14-15** - \jesus{"I am the good shepherd. I know my own..."}
  - **10:27-30** - \jesus{"My sheep hear my voice... I give them eternal life"}

### Chapter 11: Raising of Lazarus
- **11:4** - \jesus{"This illness does not lead to death..."}
- **11:7-15** - Conversation with disciples
- **11:23** - \jesus{"Your brother will rise again."}
- **11:25-26** - \jesus{"I am the resurrection and the life..."}
- **11:34** - \jesus{"Where have you laid him?"}
- **11:39-44** - Commands at the tomb
  - **11:43** - \jesus{"Lazarus, come out!"}

### Chapter 12: Triumphal Entry & Greeks Seek Jesus
- **12:7-8** - \jesus{"Leave her alone... you do not always have me"}
- **12:23-36** - Teaching about His death (like a grain of wheat)
- **12:44-50** - Final public proclamation

### Chapter 13: Upper Room - Washing Feet
- **13:7-38** - Upper Room teachings begin
  - **13:8** - \jesus{"If I do not wash you, you have no share with me"}
  - **13:13-17** - Servant leadership teaching
  - **13:21** - \jesus{"Truly, truly, I say to you, one of you will betray me"}
  - **13:31-35** - New commandment to love
  - **13:38** - Prediction of Peter's denial

### Chapter 14: Way, Truth, Life
- **14:1-31** - UPPER ROOM DISCOURSE PART 1 (ENTIRE CHAPTER is Jesus!)
  - **14:6** - \jesus{"I am the way, and the truth, and the life"}
  - **14:9** - \jesus{"Whoever has seen me has seen the Father"}
  - **14:15-17** - Promise of the Holy Spirit
  - **14:27** - \jesus{"Peace I leave with you; my peace I give to you"}

### Chapter 15: True Vine
- **15:1-27** - TRUE VINE DISCOURSE (ENTIRE CHAPTER is Jesus!)
  - **15:1** - \jesus{"I am the true vine, and my Father is the vinedresser"}
  - **15:5** - \jesus{"I am the vine; you are the branches"}
  - **15:9-17** - Abide in my love... love one another

### Chapter 16: Holy Spirit's Work
- **16:1-33** - UPPER ROOM DISCOURSE CONTINUES (ENTIRE CHAPTER is Jesus!)
  - **16:7-15** - Holy Spirit's coming and ministry
  - **16:20-22** - Sorrow to joy (childbirth metaphor)
  - **16:33** - \jesus{"In the world you will have tribulation. But take heart; I have overcome the world."}

### Chapter 17: High Priestly Prayer
- **17:1-26** - THE HIGH PRIESTLY PRAYER (ENTIRE PRAYER in red!)
  - **17:3** - \jesus{"And this is eternal life, that they know you..."}
  - **17:11** - \jesus{"Holy Father, keep them in your name..."}
  - **17:21** - \jesus{"that they may all be one..."}

### Chapter 18: Arrest & Trial
- **18:4-8** - \jesus{"Whom do you seek?... I AM... Let these men go"}
- **18:11** - \jesus{"Put your sword into its sheath..."}
- **18:20-23** - Response to high priest
- **18:34-37** - Dialog with Pilate
  - **18:36** - \jesus{"My kingdom is not of this world"}
  - **18:37** - \jesus{"You say that I am a king... everyone who is of the truth listens to my voice"}

### Chapter 19: Crucifixion
- **19:11** - \jesus{"You would have no authority over me..."}
- **19:26-27** - \jesus{"Woman, behold, your son!... Behold, your mother!"}
- **19:28** - \jesus{"I thirst."}
- **19:30** - \jesus{"It is finished."} (Τετέλεσται - MOST IMPORTANT WORDS!)

### Chapter 20: Resurrection
- **20:15** - \jesus{"Woman, why are you weeping? Whom are you seeking?"}
- **20:16** - \jesus{"Mary."}
- **20:17** - \jesus{"Do not cling to me... go to my brothers..."}
- **20:19** - \jesus{"Peace be with you."}
- **20:21-23** - Commission and Holy Spirit
- **20:26** - \jesus{"Peace be with you."}
- **20:27** - \jesus{"Put your finger here... Do not disbelieve, but believe"}
- **20:29** - \jesus{"Have you believed because you have seen me? Blessed are those who have not seen and yet have believed."}

### Chapter 21: Epilogue - Breakfast by the Sea
- **21:5-6** - \jesus{"Children, do you have any fish?... Cast the net on the right side"}
- **21:10** - \jesus{"Bring some of the fish that you have just caught."}
- **21:12** - \jesus{"Come and have breakfast."}
- **21:15-19** - Peter's restoration (THREE TIMES: "Do you love me?")
  - **21:15** - \jesus{"Simon, son of John, do you love me more than these?... Feed my lambs"}
  - **21:16** - \jesus{"Simon, son of John, do you love me?... Tend my sheep"}
  - **21:17** - \jesus{"Simon, son of John, do you love me?... Feed my sheep"}
  - **21:19** - \jesus{"Follow me."}
- **21:22** - \jesus{"If it is my will that he remain until I come, what is that to you? You follow me!"}

---

## 🎨 Visual Examples

### Example: John 14:6 (The Way, Truth, Life)

**Before** (plain text):
> Jesus said to him, "I am the way, and the truth, and the life. No one comes to the Father except through me."

**After** (with red letter):
> Jesus said to him, <span style="color:#CC0000">"I am the way, and the truth, and the life. No one comes to the Father except through me."</span>

### Example: John 11:25-26 (Resurrection and Life)

**Markdown**:
```markdown
> ^25^Jesus said to her, \jesus{"I am the resurrection and the life. Whoever believes in me, though he die, yet shall he live, ^26^and everyone who lives and believes in me shall never die. Do you believe this?"}
```

**PDF Output**:
> ^25^Jesus said to her, <span style="color:#CC0000">"I am the resurrection and the life. Whoever believes in me, though he die, yet shall he live, ^26^and everyone who lives and believes in me shall never die. Do you believe this?"</span>

---

## 📖 Guidelines for Markup

### 1. Include Quotation Marks

Always include the quotation marks inside the `\jesus{}` command:

✅ **Correct**:
```latex
\jesus{"I am the way, and the truth, and the life."}
```

❌ **Incorrect**:
```latex
"\jesus{I am the way, and the truth, and the life.}"
```

### 2. Multi-Verse Speeches

For extended discourses spanning multiple verses, wrap the entire speech:

```latex
> ^3^Jesus answered him, \jesus{"Truly, truly, I say to you, unless one is born again he cannot see the kingdom of God."} ^4^Nicodemus said to him, "How can a man be born when he is old? Can he enter a second time into his mother's womb and be born?" ^5^Jesus answered, \jesus{"Truly, truly, I say to you, unless one is born of water and the Spirit, he cannot enter the kingdom of God."}
```

### 3. Bilingual Support

Apply `\jesus{}` to **both Chinese and English** verses:

**Chinese**:
```latex
> ^6^\jesus{耶穌說：「我就是道路、真理、生命；若不藉著我，沒有人能到父那裏去。」}
```

**English**:
```latex
> ^6^Jesus said to him, \jesus{"I am the way, and the truth, and the life. No one comes to the Father except through me."}
```

### 4. Narrative vs. Direct Speech

Only mark **Jesus's direct speech** in red, not narrative descriptions:

**Example** (John 11:33):
```markdown
When Jesus saw her weeping... he was deeply moved in his spirit and greatly troubled.
```
↑ No red letter (narrative description)

**Example** (John 11:34):
```markdown
And he said, \jesus{"Where have you laid him?"}
```
↑ Red letter (direct speech)

---

## 🔍 Special Cases

### "Truly, Truly" (Ἀμὴν ἀμήν)

Always in red when Jesus says it:
```latex
\jesus{"Truly, truly, I say to you..."}
```

### "I AM" Statements (Ἐγώ εἰμι)

All seven "I AM" declarations must be in red:
1. \jesus{"I am the bread of life"} (6:35)
2. \jesus{"I am the light of the world"} (8:12)
3. \jesus{"I am the door"} (10:7, 9)
4. \jesus{"I am the good shepherd"} (10:11, 14)
5. \jesus{"I am the resurrection and the life"} (11:25)
6. \jesus{"I am the way, and the truth, and the life"} (14:6)
7. \jesus{"I am the true vine"} (15:1, 5)

### "It is finished" (Τετέλεσται)

Jesus's final word from the cross (19:30):
```latex
\jesus{"It is finished."}
```

**MUST be in red** - most important proclamation in Gospel of John!

---

## 🛠️ Technical Implementation

### LaTeX Template Code

Located in `templates/pdf/gospel-of-john-original.latex`:

```latex
%% Color Definition
\definecolor{JesusRed}{RGB}{204,0,0}  % #CC0000 - Classic red letter

%% Command Definition
\newcommand{\jesus}[1]{\textcolor{JesusRed}{#1}}
```

### Markdown to PDF Workflow

1. **Write markdown** with `\jesus{}` commands
2. **Combine chapters** via build script
3. **Pandoc processes** LaTeX commands in markdown
4. **XeLaTeX renders** with red color
5. **Output PDF** with red letter text

### Alternative: HTML/Web Version

For ai-eden.com style web display:

```css
.jesus-words {
  color: #CC0000;
  font-style: inherit;
}
```

```html
<span class="jesus-words">"I am the way, and the truth, and the life."</span>
```

---

## 📊 Coverage Statistics

| Chapter | Jesus's Words | Percentage |
|---------|---------------|------------|
| 1 | ~10 verses | 20% |
| 2 | ~5 verses | 20% |
| 3 | ~25 verses | 70% |
| 4 | ~30 verses | 60% |
| 5 | ~40 verses | 85% |
| 6 | ~50 verses | 70% |
| 7 | ~25 verses | 50% |
| 8 | ~45 verses | 75% |
| 9 | ~15 verses | 35% |
| 10 | ~35 verses | 85% |
| 11 | ~20 verses | 35% |
| 12 | ~20 verses | 40% |
| **13-17** | **Entire chapters** | **~95%** ⭐ |
| 18 | ~20 verses | 40% |
| 19 | ~8 verses | 20% |
| 20 | ~15 verses | 50% |
| 21 | ~18 verses | 70% |

**Total**: ~430+ verses of Jesus's direct speech out of 879 verses (~49% of Gospel!)

**Upper Room Discourse** (Chapters 13-17): Almost entirely Jesus's words ✝️

---

## ✅ Quality Checklist

Before publishing, verify:

- [ ] All direct quotations of Jesus are marked with `\jesus{}`
- [ ] Quotation marks are inside the command
- [ ] Both Chinese and English verses are marked
- [ ] Seven "I AM" statements are all in red
- [ ] "It is finished" (19:30) is in red
- [ ] High Priestly Prayer (Ch 17) is entirely red
- [ ] Upper Room Discourse (Ch 13-17) is mostly red
- [ ] Narrative descriptions are NOT in red (only direct speech)
- [ ] PDF renders correctly with red color

---

## 🎯 Why Red Letter?

**Historical tradition**: Started by Louis Klopsch in 1899 with the first red letter Bible

**Purpose**: Visually distinguish Jesus's words for:
- Quick reference
- Meditation focus
- Teaching emphasis
- Memorization

**ai-eden.com inspiration**: Following modern digital Bible platforms that preserve this tradition

---

**Last Updated**: 2026-01-03
**Color**: #CC0000 (RGB 204,0,0)
**Command**: `\jesus{}`
**Inspired by**: ai-eden.com
