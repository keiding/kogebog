package mdast

import (
	"bufio"
	"io"
	"regexp"
	"strings"

	"github.com/avelino/slugify"
)

type Section struct {
	Level       int
	Title       string
	Slug        string
	Text        string
	Parent      *Section
	Children    []*Section
	NextSibling *Section
}

func parseLine(str string) (text string, headerLevel int) {

	// invalid line created by bad Word formatting, remove it
	if str == "# " {
		return "", -1
	}

	r := regexp.MustCompile(`^(#+ )?(.+)$`)
	matches := r.FindStringSubmatch(str)
	if len(matches) == 3 {
		text = matches[2]
		headerLevel = len(matches[1]) - 1
	}
	return text, headerLevel
}

func Parse(in io.Reader) Section {
	doc := Section{Title: "RootOfDocument"}

	prevSection := &doc

	scanner := bufio.NewScanner(in)

	for scanner.Scan() {
		text, headerLevel := parseLine(scanner.Text())

		// Fix for empty headers
		if headerLevel > 0 && len(text) < 2 {
			continue
		}

		// if it's a header
		if headerLevel >= 1 {
			section := Section{
				Title: strings.TrimSpace(text),
				Slug:  slugify.Slugify(text),
				Level: headerLevel,
			}

			// is a heading below the previous
			if section.Level > prevSection.Level {
				section.Parent = prevSection
				if len(prevSection.Children) > 0 {
					prevSection.Children[len(prevSection.Children)-1].NextSibling = &section
				}
				prevSection.Children = append(prevSection.Children, &section)
			} else {
				for section.Level < prevSection.Level {
					prevSection = prevSection.Parent
				}
				section.Parent = prevSection.Parent
				section.Parent.Children = append(section.Parent.Children, &section)
				prevSection.NextSibling = &section
			}

			prevSection = &section

		} else {
			prevSection.Text += text + "\n"
		}
	}
	return doc
}

func Next(section *Section, stop *Section) *Section {

	if len(section.Children) > 0 {
		return section.Children[0]
	}

	for section.NextSibling == nil {
		if section.Parent == nil {
			return nil
		}
		section = section.Parent
	}

	if section == stop {
		return nil
	}

	return section.NextSibling
}
