public class Academician{
    String name;
    int age;

    public Academician(String name, int age){
        this.name =  name;
        this.age = age;
    }

    public void studentSubject(String subject){
        System.out.println(this.name + " " + this.age + " " + subject);
    }
}