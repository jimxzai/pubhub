-- Preserve Scripture carried in print-only LaTeX macros in digital formats.
local function convert(el)
  if el.format ~= 'tex' and el.format ~= 'latex' then return nil end
  local source = '\\newcommand{\\jesus}[1]{#1}\n' .. el.text
  local doc = pandoc.read(source, 'latex')
  if el.tag == 'RawBlock' then return doc.blocks end
  local result = pandoc.List()
  for _, block in ipairs(doc.blocks) do
    if block.content then result:extend(block.content) end
  end
  return result
end
return {{RawInline=convert, RawBlock=convert}}
