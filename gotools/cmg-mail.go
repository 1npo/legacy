// cmg-mailbak.go
// The tool I use to email myself a zipped backup of some files.

package main

import (
	"gopkg.in/gomail.v2"
	"archive/zip"
	"os"
	"io"
	"log"
	"bufio"
	"regexp"
)

var (
	l *log.Logger
)

type Creds struct {
	user	string
	pass	string
}

// getMRevID extracts the current revision ID string from the markdown file
// and returns it.
func getMRevID() string {
	// Open the file.
	file := os.Getenv("WDIR") + "/model.md"
	f, err := os.Open(file)
    if err != nil {
		l.Println("error:", err)
		panic(err)
	}
    defer f.Close()

	// Read each line of the file into an array, then look for a 12-digit string
	// at the very end of the file.
    var tmp []string
    rdr := bufio.NewReader(f)
    for {
        line, err := rdr.ReadString('\n')
        tmp = append(tmp, line)
        if err != nil {
            break;
        }
    }
    re := regexp.MustCompile("[0-9]{12}")
    match := re.FindStringSubmatch(tmp[len(tmp)-2])
    return match[0]
}

// sendMsg will generate a set of email headers and send the mail to me.
func sendMsg(path string, id *string) {
	a := Creds { "REDACTED", "REDACTED" }
	s := "cmg revision id " + *id
	m := gomail.NewMessage()

	m.SetHeader("From", a.user)
	m.SetHeader("To", "REDACTED")
	m.SetHeader("Subject", s)
	m.SetBody("text/html", "daily backup")
	m.Attach(path)

	d := gomail.NewPlainDialer("smtp.gmail.com", 587, a.user, a.pass)

	if err := d.DialAndSend(m); err != nil {
		l.Println("error: failed to send mail:", err)
		panic(err)
	}
}

// makeZip will zip all the files contained in the `files` array, and save the file
// as `fname`.
func makeZip(fname string, files []string) error {
	zfile, err := os.Create(fname)
	if err != nil {
		return err
	}
	defer zfile.Close()

	zwrite := zip.NewWriter(zfile)
	defer zwrite.Close()

	for _, file := range files {
		f, err := os.Open(file)
		if err != nil {
			return err
		}
		defer f.Close()

		info, err := f.Stat()
		if err != nil {
			return err
		}

		hdr, err := zip.FileInfoHeader(info)
		if err != nil {
			return err
		}

		hdr.Name = file
		hdr.Method = zip.Deflate

		w, err := zwrite.CreateHeader(hdr)
		if err != nil {
			return err
		}

		_,  err = io.Copy(w, f)
		if err != nil {
			return err
		}
	}
	return nil
}

// Set up the logging interface.
func init() {
	f, err := os.OpenFile("/home/nick/logs/backup/cmg-mailbak.log",
	os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0755)
	if err != nil {
		log.Println(err)
	}

	l = log.New(f, "cmg-mailbak: ", log.LstdFlags)
}

// Off we go!
func main() {
	mrevid := getMRevID()
	zfiles := []string{"model.md", "model.pdf"}
	zfpath := "/tmp/model-" + mrevid + ".zip"

	os.Chdir(os.Getenv("WDIR"))
	if err := makeZip(zfpath, zfiles); err != nil {
		l.Println("error: failed to zip:", err)
		return
	} else {
		l.Println("zipped files to", zfpath)
	}

	sendMsg(zfpath, &mrevid)
	l.Printf("file %v has been mailed", zfpath)

	if err := os.Remove(zfpath); err != nil {
		l.Println("error: failed to remove", zfpath)
		panic(err)
	}
}

