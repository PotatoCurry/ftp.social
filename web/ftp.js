var i = 0;
var j=0;
var k=0;
var l=0;
var m=0;
var n=0;
var o=0;
var txt = 'Welcome to ftp.social!';
var des = 'The world\'s first and only FTP-based social network!';
var reg = 'To register, upload a line-separated text file containing your username, email, and password to the registration folder. If your registration was processed successfully, you\'ll receive a confirmation email. (Not setup yet)';
var act = 'Once you\'ve signed up, login using your account and check out your home directory. You have full read/write access to your home directory (excluding the feeds folder). Although there are some special files and folders, users are generally able to freely structure their home directories. Make your home as unique and individualized as you see fit.';
var pos = 'After uploading a file to the posts folder of your home directory, the file is distributed to your followers\' feeds. Post filenames are given a date stamp within your own posts folder, and a date and user stamp in followers\' feeds. Posts cannot be directly deleted from followers\' feeds; however, there is a workaround. As date stamp will not be automatically added to a filename if it already has a manually defined date stamp, you can edit a post by editing/replacing the file in your posts folder with a file of the same name.';
var fol = 'To follow other users, upload a line-separated text file of their usernames named following.txt to your home directory. Their posts will appear in your feed directory.';
var dem = '.  .  .';
var speed1 = 20;
var speed = .001;
function load()
{
    typeWriter();
}
function typeWriter() {
  if (i < txt.length) {
    document.getElementById("welcome").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed1);  
  }
  else
    typeWriter2();
}
function typeWriter2() {
    if (j < des.length) {
      document.getElementById("description").innerHTML += des.charAt(j);
      j++;
      setTimeout(typeWriter2, speed);  
    }
    else
        typeWriter3();
  }
  function typeWriter3() {
    if (k < reg.length) {
      document.getElementById("register").innerHTML += reg.charAt(k);
      k++;
      setTimeout(typeWriter3, speed);  
    }
    else
        typeWriter4();
  }
  function typeWriter4() {
    if (l < act.length) {
      document.getElementById("accountdet").innerHTML += act.charAt(l);
      l++;
      setTimeout(typeWriter4, speed);  
    }
    else
        typeWriter5();
  }
  function typeWriter5() {
    if (m < pos.length) {
      document.getElementById("posts").innerHTML += pos.charAt(m);
      m++;
      setTimeout(typeWriter5, speed);  
    }
    else   
        typeWriter6();
  }
  function typeWriter6() {
    if (n < fol.length) {
      document.getElementById("follow").innerHTML += fol.charAt(n);
      n++;
      setTimeout(typeWriter6, speed);  
    }
    else
        typeWriter7();
  }
  function typeWriter7() {
    if (o < dem.length) {
      document.getElementById("demo").innerHTML += dem.charAt(o);
      o++;
      setTimeout(typeWriter7, speed);  
    }
  }

