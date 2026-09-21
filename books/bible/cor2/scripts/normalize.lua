-- Normalize editorial LaTeX into semantic Pandoc nodes for both formats.
function Link(el)
  local lesson = el.target:match('^(%d%d)%-[^/]+%.md$')
  if lesson then
    local number = tonumber(lesson)
    if number < 1 or number > 24 then error('Unknown lesson link: '..el.target) end
    el.target = '#lesson-'..lesson
    return el
  end
end
function RawInline(el)
  if el.format ~= 'tex' and el.format ~= 'latex' then return nil end
  local txt = el.text:gsub('\\textcolor{ScriptureGold}', '')
  local doc = pandoc.read(txt, 'latex')
  if #doc.blocks == 1 and (doc.blocks[1].t == 'Para' or doc.blocks[1].t == 'Plain') then
    if el.text:match('ScriptureGold') then
      return pandoc.Span(doc.blocks[1].content, {class='scripture-gold'})
    end
    return doc.blocks[1].content
  end
  error('Unconverted inline LaTeX: '..el.text)
end
function RawBlock(el)
  if el.format ~= 'tex' and el.format ~= 'latex' then return nil end
  if el.text:match('^\\newpage%s*$') or el.text:match('^\\backmatter%s*$') then return el end
  if el.text:match('^\\vspace') then return {} end
  local txt = el.text:gsub('\\textcolor{ScriptureGold}', ''):gsub('\\large%s*', '')
  local doc = pandoc.read(txt, 'latex')
  if el.text:match('ScriptureGold') then
    doc = doc:walk({Para = function(p)
      p.content = {pandoc.Span(p.content, {class='scripture-gold'})}
      return p
    end})
  end
  return doc.blocks
end
function Table(el)
  local heading = pandoc.utils.stringify(el.head)
  if #el.colspecs == 3 and heading:match('本章經文') and heading:match('相關經文') then
    el.colspecs = {{pandoc.AlignLeft,0.35},{pandoc.AlignLeft,0.18},{pandoc.AlignLeft,0.47}}
  end
  -- Explicit headers improve navigation and prevent empty <th> elements.
  local row = el.head.rows[1]
  if row then
    local labels = #row.cells == 3 and {'詞語／項目 Term / item', '說明 Meaning', '經文／關聯 Passage / context'} or {'項目 Item', '說明 Description'}
    for i, cell in ipairs(row.cells) do
      if pandoc.utils.stringify(cell.contents):match('^%s*$') then
        cell.contents = {pandoc.Plain({pandoc.Str(labels[i] or '項目')})}
      end
    end
  end
  return el
end
