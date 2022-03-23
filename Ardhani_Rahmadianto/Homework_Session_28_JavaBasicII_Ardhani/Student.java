public class Student extends Academician{
    String grade;
    
    public Student(String name, int age){
        super(name,age);
    }

    public void studentSubject(String subject){
        System.out.println(this.name + " " + this.age + " " + subject + " I am a Student");
    }

}